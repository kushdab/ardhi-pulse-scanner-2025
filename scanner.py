import requests
import time
import hashlib
import json
import os
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from datetime import datetime

# Configuration - In a real scenario, use environment variables
TARGET_URL = "https://www.land.go.ke/registry-updates"  # Placeholder URL
CHECK_INTERVAL = 3600  # 1 hour
DATA_FILE = "last_state.json"
LOG_FILE = "scanner.log"

# Email settings (Optional)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SCANNER_EMAIL")
SENDER_PWD = os.getenv("SCANNER_PWD")
RECEIVER_EMAIL = os.getenv("NOTIFY_EMAIL")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def get_page_hash(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ArdhiPulseScanner/2025.1'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Focus on specific registry tables or content areas to avoid false positives (like timestamps)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('main') or soup.body
        
        # Generate hash of the text content
        return hashlib.sha256(content.get_text().encode('utf-8')).hexdigest(), response.text
    except Exception as e:
        log(f"Error fetching page: {e}")
        return None, None

def send_notification(new_content):
    log("CHANGE DETECTED: Sending notification...")
    if not SENDER_EMAIL or not RECEIVER_EMAIL:
        log("Email credentials missing. Notification printed to log only.")
        return

    msg = MIMEText(f"The Ardhi Registry has been updated.\n\nCheck details at: {TARGET_URL}")
    msg['Subject'] = "[Ardhi Pulse] Land Registry Update Detected"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PWD)
        server.send_message(msg)
        server.quit()
        log("Notification email sent successfully.")
    except Exception as e:
        log(f"Failed to send email: {e}")

def run_scanner():
    log("Ardhi Pulse Scanner 2025 started.")
    
    while True:
        current_hash, html_content = get_page_hash(TARGET_URL)
        
        if current_hash:
            # Load previous state
            last_hash = ""
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    last_hash = json.load(f).get("hash", "")

            if current_hash != last_hash:
                send_notification(html_content)
                # Save new state
                with open(DATA_FILE, "w") as f:
                    json.dump({"hash": current_hash, "last_checked": str(datetime.now())}, f)
            else:
                log("No changes detected.")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_scanner()