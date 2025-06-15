# notifier.py

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# --- Slack Setup ---
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_channel = os.getenv("SLACK_DEFAULT_CHANNEL")
slack_client = WebClient(token=slack_token)

def send_slack_message(text: str):
    try:
        response = slack_client.chat_postMessage(channel=slack_channel, text=text)
        print(f"✅ Slack message sent: {response['ts']}")
    except SlackApiError as e:
        print(f"❌ Slack API error: {e.response['error']}")

# --- Gmail SMTP Setup ---
email_host = "smtp.gmail.com"  # Fixed for Gmail
email_port = 587
email_user = os.getenv("EMAIL_USER")
email_password = os.getenv("EMAIL_PASSWORD")
default_recipient = os.getenv("EMAIL_DEFAULT_RECIPIENT")

def send_email(subject: str, body: str, recipient: str = None):
    recipient = recipient or default_recipient
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Email send error: {e}")
