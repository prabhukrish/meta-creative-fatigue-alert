import os
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
ALERT_EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM")


def send_email_alert(ad):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "email": ALERT_EMAIL_FROM,
            "name": "Creative Fatigue Alert"
        },
        "to": [
            {"email": ALERT_EMAIL_TO}
        ],
        "subject": "🚨 Creative Fatigue Detected",
        "htmlContent": f"""
        <h2>Creative Fatigue Alert</h2>
        <p><strong>Ad Name:</strong> {ad['ad_name']}</p>
        <p>This creative has triggered fatigue rules.</p>
        """
    }

    headers = {
        "Accept": "application/json",
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        print("📧 Email alert sent successfully")
    else:
        print("❌ Email alert failed")
        print(response.status_code, response.text)
