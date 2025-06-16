from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def diagnose_calendar():
    creds = Credentials.from_authorized_user_file("/var/data/token.json")
    service = build("calendar", "v3", credentials=creds)

    print("DEBUG: Using Google account:",
          creds.id_token.get("email") if creds.id_token else "Unknown (id_token not present)")

    calendar_list = service.calendarList().list().execute()
    print("DEBUG: Available calendars:")
    for cal in calendar_list['items']:
        print(f" - ID: {cal['id']}")
        print(f"   Summary: {cal['summary']}")
        print(f"   Primary: {cal.get('primary', False)}")
        print("-" * 40)

def calendar_agent(final_state):
    diagnose_calendar()
    print("DEBUG: final_state received:", final_state)
    print("DEBUG: final_state['daily_schedule']:", final_state.get("daily_schedule"))

    creds = Credentials.from_authorized_user_file("/var/data/token.json")
    service = build("calendar", "v3", credentials=creds)

    for item in final_state.get("daily_schedule", []):
        event = {
            "summary": item["summary"],
            "start": {"dateTime": item["start"], "timeZone": "UTC"},
            "end": {"dateTime": item["end"], "timeZone": "UTC"}
        }
        print("DEBUG: Creating event:", event)
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print("DEBUG: Event created with ID:", created_event.get("id"))

    return {"calendar_confirmation": "Events created successfully"}
