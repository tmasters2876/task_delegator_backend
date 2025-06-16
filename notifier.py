import os
from slack_sdk import WebClient

def send_slack_reminders(tasks):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_DEFAULT_CHANNEL")

    if not slack_token or not slack_channel:
        print("Slack credentials missing")
        return

    client = WebClient(token=slack_token)

    for task in tasks:
        message = f":bell: Reminder: {task['summary']} - {task['start']}"
        response = client.chat_postMessage(channel=slack_channel, text=message)
        print(f"Slack response: {response}")
