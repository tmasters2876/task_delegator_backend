import re
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os

def calendar_agent(state):
    schedule_text = state.get("daily_schedule", "")
    lines = schedule_text.splitlines()
    calendar_confirmation = []

    # ✅ Use Render disk paths
    creds = Credentials.from_authorized_user_info(
        json.loads(open("/var/data/token.json").read()),
        scopes=["https://www.googleapis.com/auth/calendar.events"]
    )
    service = build("calendar", "v3", credentials=creds)

    today = datetime.now().date()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Normalize dashes
        line = line.replace("–", "-").replace("—", "-")

        # Pattern: start - end - title
        match = re.match(r"(\d{1,2}:\d{2}\s?[APMapm]{2})\s*-\s*(\d{1,2}:\d{2}\s?[APMapm]{2})\s*-\s*(.+)", line)
        if match:
            start_str, end_str, summary = match.groups()
        else:
            # Fallback: single time - title
            match = re.match(r"(\d{1,2}:\d{2}\s?[APMapm]{2})\s*-\s*(.+)", line)
            if match:
                start_str, summary = match.groups()
                start_time = datetime.strptime(start_str.strip(), "%I:%M %p")
                end_time = start_time + timedelta(hours=1)
                end_str = end_time.strftime("%I:%M %p")
            else:
                calendar_confirmation.append(f"⚠️ Skipped: {line}")
                continue

        try:
            start_dt = datetime.strptime(start_str.strip(), "%I:%M %p")
            end_dt = datetime.strptime(end_str.strip(), "%I:%M %p")
        except Exception:
            calendar_confirmation.append(f"❌ Time parse failed: {line}")
            continue

        start_datetime = datetime.combine(today, start_dt.time())
        end_datetime = datetime.combine(today, end_dt.time())

        event = {
            "summary": summary.strip(),
            "start": {"dateTime": start_datetime.isoformat(), "timeZone": "America/Chicago"},
            "end": {"dateTime": end_datetime.isoformat(), "timeZone": "America/Chicago"},
        }

        try:
            created_event = service.events().insert(calendarId="primary", body=event).execute()
            calendar_confirmation.append(f"✅ {summary.strip()} ({start_str} – {end_str})")
        except Exception as e:
            calendar_confirmation.append(f"❌ Failed to create event: {summary.strip()} — {str(e)}")

    return {"calendar_confirmation": "\n".join(calendar_confirmation)}
