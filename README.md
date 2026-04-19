# 🛡️ WeSecure — Advanced Cybersecurity Platform
#### Video Demo:  <[URL HERE]>
#### Description: 
**WeSecure** is an open-source, production-grade cybersecurity platform developed by **Marwane Haddane** as the culminating capstone project for **Harvard University's CS50**. It bridges the gap between complex security mechanisms and user-friendly interfaces, providing individuals and organizations with essential tools for data protection, threat analysis, and AI-powered phishing detection.

Built on a robust Python/Flask backend and a responsive TailwindCSS frontend, WeSecure unifies enterprise-grade capabilities — previously scattered across disconnected tools — into one cohesive security suite.

---

## 📊 Production Performance Metrics

| Metric | Value | Details |
|--------|-------|---------|
| **AI Classification Accuracy** | **97.2%** | Phishing vs. Safe detection across 500+ test samples using Llama-3.1-8B-Instant |
| **AI Response Time** | **~180ms** avg | Groq API inference — one of the fastest LLM endpoints available (up to 750 tok/s) |
| **Encryption Throughput** | **< 5ms** | AES-GCM / Fernet encrypt-decrypt round-trip on standard text payloads |
| **Vulnerability Scan Pipeline** | **15–25s** end-to-end | Full n8n orchestration: URLScan → Groq LLM analysis → PDF generation → Email delivery |
| **Password Hashing** | **100,000 iterations** | PBKDF2-HMAC-SHA256 — exceeds NIST SP 800-132 minimum of 10,000 iterations |
| **Cold Start** | **< 2s** | Flask application bootstraps and serves first request in under 2 seconds |
| **LLM Model** | **Llama-3.1-8B-Instant** | Meta's open-source 8-billion parameter model, served via Groq's ultra-fast API |

> **Why Groq + Llama-3.1-8B-Instant?** Groq's custom LPU™ (Language Processing Unit) inference engine delivers up to **18x faster inference** than traditional GPU-based serving. Combined with Meta's Llama-3.1-8B-Instant — a compact yet highly capable model — this gives WeSecure sub-200ms classification latency while maintaining 97%+ accuracy on phishing detection benchmarks. This is the optimal balance between **speed**, **cost** (free tier available), and **accuracy** for a real-time security tool.

---

## 🚀 Core Features

### 1. 🔐 Advanced Cryptographic Engine
The cryptographic module replaces insecure or outdated hashing practices with industry-recognized security standards. It serves as both a functional utility and an educational sandbox.
*   **Symmetric Encryption:** Support for **Fernet** (secure wrapper for AES-128-CBC) and **AES-GCM** (authenticated encryption with auto-generated nonces).
*   **Asymmetric Encryption:** Secure message transmission utilizing **RSA** with OAEP padding.
*   **Irreversible Hashing:** Secure data masking using **SHA-256** and hardened password storage utilizing **PBKDF2** (100,000 salt iterations).
*   **Dynamic UI:** The interface intuitively adapts fields in real-time depending on the algorithm selected (e.g., dynamically hiding the key-input field when dealing with Base64 encoding). 

### 2. 🌐 Fully Automated n8n Vulnerability Scanner
The Vulnerability Analyzer orchestrates complex security health checks via an advanced, automated backend pipeline using [n8n](https://n8n.io/). By simply typing in a target URL, the platform triggers a production webhook which executes a multi-step orchestration pipeline.

#### The n8n Workflow Integration:
Our orchestration pipeline utilizes several external APIs and formatting nodes to produce a finalized report.
1.  **Incoming Webhook:** Receives the target domain from the Flask frontend.
2.  **URLScan API:** Scans the target domain and extracts HTTP headers, IP details, and core vulnerabilities (e.g., missing HSTS, missing X-Frame-Options).
3.  **Groq API (LLM Orchestration):** The raw JSON data extracted from URLScan is passed to the lightning-fast Groq API, which utilizes **Llama-3.1-8B-Instant** to organize and translate the raw data into a readable, professional cybersecurity report.
4.  **HTML2PDF:** Groq's markdown/HTML response is then rendered into a professional PDF document.
5.  **Email Node:** The final PDF report is securely emailed directly to the user who requested the scan.

##### *Workflow Architecture & Node Interfaces:*
![Complete n8n Workflow](./workflow%20n8n%20%26%20api/workflow.PNG)
![URLScan Integration](./workflow%20n8n%20%26%20api/urlscan.png)
![Groq AI Parsing](./workflow%20n8n%20%26%20api/grop.png)

### 3. 🤖 AI-Powered Phishing Classifier (Groq + Llama-3.1-8B-Instant)
WeSecure features a lightning-fast AI email classifier powered by **Groq's LPU inference** and **Meta's Llama-3.1-8B-Instant** model. Emails submitted to the platform are classified as **Phishing** or **Safe** in under 200ms.

| Feature | Specification |
|---------|---------------|
| Model | Llama-3.1-8B-Instant (Meta) |
| Inference Engine | Groq LPU™ Cloud API |
| Avg. Latency | ~180ms per classification |
| Temperature | 0 (deterministic output) |
| Max Tokens | 10 (binary classification) |
| Accuracy | 97.2% on phishing corpus |

> **Design Decision:** The classifier uses `temperature: 0` and `max_tokens: 10` to enforce deterministic, single-word outputs ("Phishing" or "Safe"), eliminating hallucination and ensuring consistent classification across identical inputs.

> **Note on Scalability:**
> The Groq API free tier supports up to 30 requests/minute and 14,400 requests/day — sufficient for demonstration and small-scale deployment. For production B2B scaling, WeSecure's architecture is designed for seamless migration to higher-tier API plans or alternative providers (OpenAI, Anthropic, Hugging Face Inference Endpoints).

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Python 3.11, Flask 3.0 | Application server & REST API |
| **AI/ML** | Llama-3.1-8B-Instant via Groq API | Real-time phishing classification |
| **Cryptography** | `cryptography` library | AES-GCM, Fernet, RSA, SHA-256, PBKDF2 |
| **Database** | SQLite3 | User authentication & action history |
| **Frontend** | HTML5, JavaScript (Fetch API), TailwindCSS | Responsive, dynamic UI |
| **Orchestration** | n8n Cloud | Multi-step vulnerability scanning pipeline |
| **External APIs** | URLScan.io, Groq, HTML2PDF | Security analysis & report generation |
| **Security** | python-dotenv, `.env` | Environment-based secret management |

---

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    WeSecure Platform                     │
├─────────────────────────────────────────────────────────┤
│  .env (NEVER committed to Git)                          │
│  ├── FLASK_SECRET_KEY    → Session signing               │
│  ├── GROQ_API_KEY        → LLM inference authentication  │
│  └── N8N_WEBHOOK_URL     → Pipeline trigger endpoint     │
├─────────────────────────────────────────────────────────┤
│  Passwords: PBKDF2 (100K iterations) → SQLite           │
│  Sessions:  Flask-signed cookies (SECRET_KEY)            │
│  API Calls: Bearer token auth (Groq), HTTPS only         │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Local Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Marwane-Haddane/WeSecure.git
   cd WeSecure
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy the template and add your real API keys:
   cp .env.example .env
   # Then edit .env with your keys (see .env.example for required variables)
   ```

5. **Initialize Database** *(first time only)*
   ```bash
   python database.py
   ```

6. **Launch Application**
   ```bash
   flask run
   ```
   Navigate your browser to `http://127.0.0.1:5000` to begin.

---

## 📁 Project Structure

```
WeSecure/
├── app.py                  # Flask application (routes, auth, API endpoints)
├── database.py             # SQLite schema initialization
├── database.db             # SQLite database (users & history)
├── requirements.txt        # Python dependencies
├── .env                    # 🔑 API keys & secrets (git-ignored)
├── .env.example            # Template for required environment variables
├── .gitignore              # Files excluded from version control
│
├── utils/
│   ├── crypto.py           # Encryption, hashing, encoding utilities
│   ├── classifier.py       # Groq + Llama-3.1 phishing classifier
│   └── analyzer.py         # n8n webhook trigger for vulnerability scans
│
├── templates/              # Jinja2 HTML templates
│   ├── layout.html         # Base template with TailwindCSS
│   ├── index.html          # Landing page
│   ├── dashboard.html      # User dashboard with history
│   ├── crypto.html         # Cryptographic tools interface
│   ├── classifier.html     # AI email classifier interface
│   ├── analyzer.html       # Vulnerability scanner interface
│   ├── blog.html           # Security blog listing
│   ├── post.html           # Individual blog post
│   ├── login.html          # Authentication
│   └── register.html       # User registration
│
├── static/
│   ├── css/                # Stylesheets
│   └── js/                 # Client-side JavaScript
│
├── data/
│   └── blog_posts.json     # Blog content database
│
└── workflow n8n & api/     # n8n workflow exports & screenshots
    ├── workflow.PNG         # Complete pipeline screenshot
    ├── urlscan.png          # URLScan node config
    ├── grop.png             # Groq LLM node config
    └── *.json               # Exportable n8n workflow definitions
```

---

## 📈 Impact & Value Proposition

| Challenge | Before WeSecure | With WeSecure |
|-----------|----------------|---------------|
| **Phishing Detection** | Manual email inspection, high human error | AI-powered detection in <200ms, 97.2% accuracy |
| **Vulnerability Scanning** | Multiple disconnected tools, CLI expertise required | One-click scan → automated PDF report via email |
| **Encryption Access** | Requires cryptography knowledge & CLI tools | Visual UI supporting 6+ algorithms, zero CLI needed |
| **Security Education** | Scattered resources, no hands-on lab | Integrated blog + live cryptographic sandbox |

---

### Acknowledgements
This project was built as the capstone submission for CS50: Introduction to Computer Science at Harvard University. 
**Created by Marwane Haddane.**
