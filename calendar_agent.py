import os
import datetime
import pytz
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# === CONFIG ===
CREDENTIALS_PATH = "/var/data/credentials.json"
TOKEN_PATH = "/var/data/token.json"

def calendar_agent(final_state):
    """
    Creates Google Calendar events based on the final_state's daily_schedule.
    Uses OAuth credentials stored in /var/data.
    """

    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
        service = build("calendar", "v3", credentials=creds)

        timezone = "America/Chicago"

        for item in final_state.daily_schedule:
            event = {
                "summary": item.get("summary", "Task"),
                "description": item.get("description", ""),
                "start": {
                    "dateTime": item.get("start"),
                    "timeZone": timezone,
                },
                "end": {
                    "dateTime": item.get("end"),
                    "timeZone": timezone,
                },
            }

            service.events().insert(calendarId="primary", body=event).execute()

        # ✅ GUARANTEED RETURN
        return {"calendar_confirmation": "Events created successfully"}

    except Exception as e:
        print(f"Calendar Agent Error: {e}")
        return {"calendar_confirmation": f"Error: {e}"}
