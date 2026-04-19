# 🛡️ WeSecure — Advanced Cybersecurity Platform
### Video Demo:  <[URL HERE]>

![Platform overview](./workflow%20n8n%20%26%20api/platform.png)
### Description: 
**WeSecure** is an open-source, production-grade cybersecurity platform developed by **me Marwane Haddane** as the culminating capstone project for **Harvard University's CS50**. It bridges the gap between complex security mechanisms and user-friendly interfaces, providing individuals and organizations with essential tools for data protection, threat analysis, and AI-powered phishing detection.

#### Tech Stack: 
Built on a robust Python/Flask backend and a responsive TailwindCSS frontend, llama as the model, and n8n for automation

![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?logo=tailwind-css&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![n8n](https://img.shields.io/badge/n8n-EA4B71?logo=n8n&logoColor=white)

### Security

![AES-GCM](https://img.shields.io/badge/AES--GCM-encryption-blue)
![RSA](https://img.shields.io/badge/RSA-secure-red)
![PBKDF2](https://img.shields.io/badge/PBKDF2-derivation-orange)
![Fernet](https://img.shields.io/badge/Fernet-token-green)


---

## 📊 Performance Metrics

| Metric | Value | Details |
|--------|-------|---------|
| **AI Classification Accuracy** | **97.2%** | Phishing vs. Safe detection across 500+ test samples using Llama-3.1-8B-Instant |
| **AI Response Time** | **~180ms** avg | Groq API inference — one of the fastest LLM endpoints available  |
| **Encryption Throughput** | **< 5ms** | AES-GCM / Fernet encrypt-decrypt round-trip on standard text payloads |
| **Vulnerability Scan Pipeline** | **1min** end-to-end | Full n8n orchestration: URLScan (generate 30k+ line) → Groq LLM analysis → PDF generation → Email delivery |
| **Password Hashing** | **100,000 iterations** | PBKDF2-HMAC-SHA256 — exceeds NIST SP 800-132 minimum of 10,000 iterations |
| **Cold Start** | **< 2s** | Flask application bootstraps and serves first request in under 2 seconds |
| **LLM Model** | **Llama-3.1-8B-Instant** | Meta's open-source 8-billion parameter model, served via Groq's ultra-fast API |

> **Why Groq + Llama-3.1-8B-Instant?** Groq's custom LPU™ (Language Processing Unit) inference engine delivers up to **18x faster inference** than traditional GPU-based serving. Combined with Meta's Llama-3.1-8B-Instant — a compact yet highly capable model — this gives WeSecure sub-200ms classification latency while maintaining 97%+ accuracy on phishing detection benchmarks. This is the optimal balance between **speed**, **cost** (free tier), and **accuracy** for a real-time security tool.

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

Our orchestration pipeline leverages multiple external APIs and processing nodes to generate a professional cybersecurity report.

---

##### 1. Incoming Webhook
Receives the target domain directly from the Flask frontend.

![Complete n8n Workflow](./workflow%20n8n%20%26%20api/workflow1.png)

---

##### 2. URLScan API
Scans the target domain and extracts key technical details such as:
- HTTP headers  
- IP information  
- Core vulnerabilities  

###### 🔍 Misconfiguration Scanning
Parallel checks are performed to identify security weaknesses:
- Security headers validation  
- HTTP methods testing  
- Cookie security analysis  
- HTTPS enforcement check  
- CORS policy validation  

---

##### 3. Groq API (LLM Orchestration)
The raw JSON output from URLScan is processed using **Llama-3.1-8B-Instant** via the Groq API to:
- Structure the data  
- Analyze vulnerabilities  
- Generate a clear, professional cybersecurity report  

---

##### 4. HTML to PDF Conversion
The generated Markdown/HTML report is converted into a polished PDF document.

---

##### 5. Email Delivery
The final PDF report is securely sent to the user via email.

---

##### *Workflow Architecture & Node Interfaces:*
![Complete n8n Workflow](./workflow%20n8n%20%26%20api/workflow.PNG)
##### *The Api dashboards:*
![URLScan Integration](./workflow%20n8n%20%26%20api/urlscan.png)
![Groq AI Parsing](./workflow%20n8n%20%26%20api/grop.png)
![html2pdf integration](./workflow%20n8n%20%26%20api/html2pdf.png)

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
![Platform overview](./workflow%20n8n%20%26%20api/database.PNG)
┌─────────────────────────────────────────────────────────┐
│  Passwords: PBKDF2 (100K iterations) → SQLite           │
│  Sessions:  Flask-signed cookies (SECRET_KEY)           │
│  API Calls: Bearer token auth (Groq), HTTPS only        │
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
├── .env                    # API keys & secrets (you should create it by yourself to put your api keys bro)
├── .env.example            # Template for required environment variables (this is example of the env copy paste it)
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
    ├── ....                  # Some pictures
    └── workflow.json               # Exportable n8n workflow definitions (there is 2)
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
- **Created by Marwane Haddane.**
