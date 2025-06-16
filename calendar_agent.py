from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def calendar_agent(final_state):
    # Load credentials from the mounted disk
    creds = Credentials.from_authorized_user_file("/var/data/token.json")

    # Build the Google Calendar service client
    service = build("calendar", "v3", credentials=creds)

    # ✅ Debug: show which Google account is being used (if ID token exists)
    print("DEBUG: Using Google account:",
          creds.id_token.get("email") if creds.id_token else "Unknown (id_token not present)")

    # Loop through each scheduled item and create a calendar event
    for item in final_state["daily_schedule"]:
        event = {
            "summary": item["summary"],
            "start": {
                "dateTime": item["start"],
                "timeZone": "UTC"  # You can adjust timezone as needed
            },
            "end": {
                "dateTime": item["end"],
                "timeZone": "UTC"
            }
        }

        # ✅ Debug: show the event payload before sending
        print("DEBUG: Creating event:", event)

        # Call Google Calendar API to insert the event
        created_event = service.events().insert(calendarId="primary", body=event).execute()

        # ✅ Debug: show the response ID to confirm it was created
        print("DEBUG: Event created with ID:", created_event.get("id"))

    # Return a standard confirmation for API response
    return {"calendar_confirmation": "Events created successfully"}
