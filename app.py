import os
from dotenv import load_dotenv
load_dotenv()
import sqlite3
import json
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Import utilities
from utils.crypto import hash_text, generate_key, encrypt_text, decrypt_text, process_encoding
from utils.analyzer import send_n8n_analysis
from utils.classifier import classify_email

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Secret key for session signing
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-fallback-key")

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
BLOG_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'blog_posts.json')

def get_db_connection():
    """Helper to connect to the SQLite DB."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def log_history(user_id, action, result):
    """Logs user actions to the database."""
    conn = get_db_connection()
    conn.execute("INSERT INTO history (user_id, action, result) VALUES (?, ?, ?)",
                 (user_id, action, result))
    conn.commit()
    conn.close()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# ==============================
# AUTHENTICATION ROUTES
# ==============================

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Must provide username and password", "error")
            return render_template("login.html")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username and/or password", "error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["user_email"] = user["email"]

        # Ensure user has an encryption key for this session
        if "crypto_key" not in session:
            session["crypto_key"] = generate_key()

        return redirect(url_for("dashboard"))

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")
        elif password != confirmation:
            flash("Passwords must match.", "error")
            return render_template("register.html")

        # Hash the password
        hash_pwd = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                         (username, email, hash_pwd))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
            conn.close()
            return render_template("register.html")
        
        conn.close()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect(url_for("index"))


# ==============================
# MAIN ROUTES
# ==============================

@app.route("/")
def index():
    """Landing Page"""
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    """Show dashboard and Recent History"""
    conn = get_db_connection()
    history_records = conn.execute(
        "SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    
    return render_template("dashboard.html", username=session.get("username"), history=history_records)


# ==============================
# TOOLS API ROUTES (AJAX)
# ==============================

@app.route("/crypto", methods=["GET", "POST"])
@login_required
def crypto():
    """Interface to cryptographic tools"""
    if request.method == "POST":
        data = request.json
        action = data.get("action")  # encrypt, decrypt, hash, encode, decode
        algorithm = data.get("algorithm") # fernet, rsa, aes_gcm, sha256, pbkdf2, base64
        input_text = data.get("text")
        user_key = data.get("key")
        
        if not input_text:
            return jsonify({"status": "error", "message": "Input text required."}), 400

        # Optional: fallback to session key if they left it blank
        if not user_key and action in ["encrypt", "decrypt"] and algorithm in ["fernet", "aes_gcm"]:
            user_key = session.get("crypto_key")

        result = ""
        
        if action == "hash":
            result = hash_text(input_text, algorithm)
            log_history(session["user_id"], f"Hash ({algorithm})", result[:20] + "...")
            
        elif action == "encrypt":
            result = encrypt_text(input_text, algorithm, user_key)
            if "Error" in result:
                return jsonify({"status": "error", "message": result}), 400
            log_history(session["user_id"], f"Encrypt ({algorithm})", "Encrypted string")
            
        elif action == "decrypt":
            result = decrypt_text(input_text, algorithm, user_key)
            if "Error" in result:
                return jsonify({"status": "error", "message": result}), 400
            log_history(session["user_id"], f"Decrypt ({algorithm})", "Decrypted string")
            
        elif action == "encode":
            result = process_encoding(input_text, algorithm, decode=False)
            if "Error" in result:
                return jsonify({"status": "error", "message": result}), 400
            log_history(session["user_id"], f"Encode ({algorithm})", "Encoded string")
            
        elif action == "decode":
            result = process_encoding(input_text, algorithm, decode=True)
            if "Error" in result:
                return jsonify({"status": "error", "message": result}), 400
            log_history(session["user_id"], f"Decode ({algorithm})", "Decoded string")

        else:
            return jsonify({"status": "error", "message": "Invalid action."}), 400

        return jsonify({"status": "success", "result": result})
        
    # GET method
    return render_template("crypto.html")


@app.route("/analyzer", methods=["GET", "POST"])
@login_required
def analyzer():
    """Analyzer module with n8n webhook API Call."""
    if request.method == "POST":
        data = request.json
        target_url = data.get("url")
        email_override = data.get("email")

        if not target_url:
             return jsonify({"status": "error", "message": "URL is required for analysis."}), 400
             
        # Decide which email to use
        target_email = email_override if email_override else session.get("user_email")
        
        # Trigger n8n webhook
        response = send_n8n_analysis(target_url, target_email)
        
        if response["status"] == "success":
            log_history(session["user_id"], f"Analysis Triggered", f"URL: {target_url}")
            return jsonify(response)
        else:
            return jsonify(response), 400

    # GET method
    return render_template("analyzer.html", default_email=session.get("user_email"))


@app.route("/classifier", methods=["GET", "POST"])
@login_required
def classifier():
    """Llama-based Email Classifier API Call."""
    if request.method == "POST":
        data = request.json
        email_content = data.get("email_content")

        if not email_content:
             return jsonify({"status": "error", "message": "Email content is required."}), 400
             
        # Trigger Llama classification
        result = classify_email(email_content)
        
        if result.startswith("Error"):
            return jsonify({"status": "error", "message": result}), 500
        else:
            log_history(session["user_id"], f"Email Classified", f"Result: {result}")
            return jsonify({"status": "success", "classification": result})

    # GET method
    return render_template("classifier.html")


# ==============================
# BLOG ROUTES
# ==============================

@app.route("/blog")
def blog():
    """Displays the list of blog posts."""
    try:
        with open(BLOG_JSON_PATH, "r") as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    
    return render_template("blog.html", posts=posts)


@app.route("/blog/<int:post_id>")
def post(post_id):
    """Displays an individual blog post."""
    try:
        with open(BLOG_JSON_PATH, "r") as file:
            posts = json.load(file)
            # Find specific post
            post_data = next((p for p in posts if p["id"] == post_id), None)
            if post_data is None:
                return "Post not found", 404
            
    except FileNotFoundError:
        return "Blog DB not found", 404

    return render_template("post.html", post=post_data)

if __name__ == "__main__":
    app.run(debug=True)
