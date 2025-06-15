import datetime
import os.path
import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def calendar_agent(final_state):
    creds = None
    creds_path = "/var/data/credentials.json"
    token_path = "/var/data/token.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        if os.path.exists(creds_path):
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    for item in final_state.daily_schedule:
        event = {
            'summary': item.get("summary"),
            'location': '',
            'description': item.get("description"),
            'start': {
                'dateTime': item.get("start"),
                'timeZone': 'America/Chicago',
            },
            'end': {
                'dateTime': item.get("end"),
                'timeZone': 'America/Chicago',
            },
        }

        service.events().insert(calendarId='primary', body=event).execute()

    # ✅ Only addition: guaranteed return so Flask never crashes
    return {"calendar_confirmation": "Events created successfully"}
