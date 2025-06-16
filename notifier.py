import os
from slack_sdk import WebClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_reminder(subject, body):
    sender_email = os.environ.get("EMAIL_SENDER")
    receiver_email = os.environ.get("EMAIL_RECEIVER")
    email_password = os.environ.get("EMAIL_PASSWORD")

    print(f"DEBUG: EMAIL_SENDER={sender_email}, EMAIL_RECEIVER={receiver_email}")

    if not sender_email or not receiver_email or not email_password:
        print("Email credentials missing — skipping send.")
        return

    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, email_password)
            server.send_message(message)

        print("DEBUG: Email sent successfully.")
    except Exception as e:
        print(f"Email send failed: {e}")

def send_slack_reminders(tasks):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_DEFAULT_CHANNEL")
    if not slack_token or not slack_channel:
        print("Slack credentials missing.")
        return

    client = WebClient(token=slack_token)
    for task in tasks:
        message = f":bell: Reminder: {task['summary']} - {task['start']}"
        response = client.chat_postMessage(channel=slack_channel, text=message)
        print(f"Slack response: {response}")
