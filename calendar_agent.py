from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

def calendar_agent(final_state):
    # Use env var path if set, else fallback to local dev default
    token_path = os.environ.get("GOOGLE_TOKEN_PATH", "token.json")
    print(f"✅ DEBUG: Using token path: {token_path}")

    creds = Credentials.from_authorized_user_file(token_path)
    service = build("calendar", "v3", credentials=creds)

    # Debug: confirm which account
    if creds.id_token:
        print("✅ DEBUG: Authenticated Google account:", creds.id_token.get("email"))
    else:
        print("⚠️ DEBUG: No ID token found — using refresh_token only.")

    schedule = final_state.get("daily_schedule", [])
    print(f"✅ DEBUG: Number of events to insert: {len(schedule)}")

    for item in schedule:
        event = {
            "summary": item["summary"],
            "start": {"dateTime": item["start"], "timeZone": "UTC"},
            "end": {"dateTime": item["end"], "timeZone": "UTC"}
        }
        print("➡️ DEBUG: Creating event:", event)
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print("✅ DEBUG: Event created with ID:", created_event.get("id"))

    return {"calendar_confirmation": "Events created successfully"}
