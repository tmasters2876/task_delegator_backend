import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def calendar_agent(final_state):
    creds = None
    if os.path.exists("/var/data/token.json"):
        creds = Credentials.from_authorized_user_file("/var/data/token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return {"calendar_confirmation": "No valid Google credentials"}

    service = build("calendar", "v3", credentials=creds)

    for item in final_state["daily_schedule"]:  # ✅ corrected for dict
        event = {
            "summary": item["summary"],
            "start": {
                "dateTime": item["start"],
                "timeZone": "America/Chicago",
            },
            "end": {
                "dateTime": item["end"],
                "timeZone": "America/Chicago",
            },
        }
        service.events().insert(calendarId="primary", body=event).execute()

    return {"calendar_confirmation": "Events created successfully"}
