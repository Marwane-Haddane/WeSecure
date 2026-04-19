import os
import requests

# n8n Webhook URL loaded from .env file
WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "https://marwane-x-cs50.app.n8n.cloud/webhook/scan-report")

def send_n8n_analysis(target_url, email="[wesecure.report@gmail.com]"):
    """
    Sends a request to the n8n webhook to trigger an analysis.
    If email is not provided, it will use a default or assume the webhook handles it.
    """
    payload = {
        "url": target_url
    }
    
    if email:
        payload["email"] = email

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        # Even if webhook returns 200, we'll return a success dict
        return {"status": "success", "message": "Report sent successfully"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Failed to connect to analyzer: {str(e)}"}
