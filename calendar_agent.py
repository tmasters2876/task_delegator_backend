from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

def calendar_agent(final_state):
    # Use Render disk path or fallback
    token_path = os.getenv("GOOGLE_TOKEN_PATH", "/var/data/token.json")
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "/var/data/credentials.json")

    print(f"✅ Using token at: {token_path}")
    print(f"✅ Using credentials at: {credentials_path}")

    creds = Credentials.from_authorized_user_file(token_path)
    service = build("calendar", "v3", credentials=creds)

    print(f"✅ Authenticated as: {creds.id_token.get('email') if creds.id_token else 'Unknown'}")

    for item in final_state.get("daily_schedule", []):
        event = {
            "summary": item["summary"],
            "start": {
                "dateTime": item["start"],
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": item["end"],
                "timeZone": "UTC"
            }
        }
        print(f"➡️ Creating event: {event}")
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"✅ Created event ID: {created_event.get('id')}")

    return {"calendar_confirmation": "Events created successfully"}
