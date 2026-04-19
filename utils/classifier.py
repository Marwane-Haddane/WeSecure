import os
import requests

# Groq API Key loaded from .env file
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def classify_email(email_content):
    """
    Classifies an email as 'Phishing' or 'Safe' using Llama-3 via Groq API.
    """
    if not GROQ_API_KEY:
        return "Error: Please set your GROQ_API_KEY in the .env file before scanning."

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """
You are a highly accurate cybersecurity email classifier. 
Your task is to assign the provided email to EXACTLY ONE of the following categories:
- Phishing: Suspicious emails attempting to steal credentials, fake password resets, malicious attachments, or urgent requests for money/data.
- Safe: Normal emails like verified promotions, personal communication, or standard service updates.

Respond with ONLY the word "Phishing" or "Safe". Do not include extra text, explanations, or punctuation.
"""

    payload = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0,
        "max_tokens": 10,
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": f"Email to classify:\n\n{email_content}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code != 200:
            return f"Error connecting to Groq: {response.text}"
            
        data = response.json()
        result = data['choices'][0]['message']['content'].strip()
        
        # Parse the result carefully to ensure we only return Phishing or Safe
        if "phishing" in result.lower():
            return "Phishing"
        elif "safe" in result.lower():
            return "Safe"
        else:
            return f"Unknown (Model output: {result})"
            
    except Exception as e:
         return f"Error: {str(e)}"
