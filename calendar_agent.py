from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def calendar_agent(final_state):
    try:
        # Safe inspection of final_state to avoid silent crashes
        print("DEBUG: Received final_state keys:", list(final_state.keys()))
        schedule = final_state.get("daily_schedule", [])
        print("DEBUG: Number of events to insert:", len(schedule))

        # Load calendar credentials
        creds = Credentials.from_authorized_user_file("/var/data/token.json")
        service = build("calendar", "v3", credentials=creds)

        # Show email associated with this token, if available
        if creds.id_token:
            print("DEBUG: Authenticated Google account:", creds.id_token.get("email"))
        else:
            print("DEBUG: No ID token found in credentials.")

        # Insert calendar events
        for item in schedule:
            event = {
                "summary": item["summary"],
                "start": {"dateTime": item["start"], "timeZone": "UTC"},
                "end": {"dateTime": item["end"], "timeZone": "UTC"}
            }
            print("DEBUG: Inserting event:", event)
            created_event = service.events().insert(calendarId="primary", body=event).execute()
            print("DEBUG: Created event ID:", created_event.get("id"))

        return {"calendar_confirmation": "Events created successfully"}

    except Exception as e:
        print("❌ ERROR in calendar_agent:", str(e))
        return {"calendar_confirmation": f"Failed due to: {str(e)}"}
