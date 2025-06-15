from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from notifier import send_slack_message, send_email
from datetime import datetime


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def intake_agent(state):
    return {"raw_input": state.raw_input}

def classifier_agent(state):
    prompt = f"Categorize tasks:\n{state.raw_input}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )
    raw_content = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw_content)
        return {"classified_tasks": parsed.get("classified_tasks", raw_content)}
    except Exception:
        return {"classified_tasks": raw_content}

def optimizer_agent(state):
    prompt = f"Optimize sequence:\n{state.classified_tasks}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.4
    )
    raw_content = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw_content)
        return {"optimized_tasks": parsed.get("optimized_tasks", raw_content)}
    except Exception:
        return {"optimized_tasks": raw_content}

def delegator_agent(state):
    prompt = f"Delegate each task to Self, Assistant, Family, or External:\n{state.optimized_tasks}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.4
    )
    raw_content = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw_content)
        return {"delegated_tasks": parsed.get("delegated_tasks", raw_content)}
    except Exception:
        return {"delegated_tasks": raw_content}

def priority_agent(state):
    prompt = f"Prioritize each delegated task as High, Medium, or Low:\n{state.delegated_tasks}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.4
    )
    raw_content = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw_content)
        return {"prioritized_tasks": parsed.get("prioritized_tasks", raw_content)}
    except Exception:
        return {"prioritized_tasks": raw_content}

def planner_agent(state):
    context_note = f"Context: {state.daily_context}\n" if state.daily_context else ""

    # Calculate a smart anchor start time: now rounded to next 30min
    now = datetime.now()
    rounded_minute = 30 if now.minute >= 30 else 0
    start_hour = now.hour if rounded_minute == 0 else (now.hour + 1)
    start_time_str = f"{start_hour % 12 or 12}:{rounded_minute:02d} {'AM' if start_hour < 12 else 'PM'}"

    prompt = (
        f"{context_note}"
        f"You are a personal day planner. Use the following tasks to create a practical daily plan.\n\n"
        f"Tasks:\n{state.prioritized_tasks}\n\n"
        f"- Anchor start time: {start_time_str}\n"
        f"- Fill remaining time with reasonable breaks, meals, or rest if needed.\n"
        f"- Format: 'HH:MM AM/PM - HH:MM AM/PM - Task'\n"
        f"- Keep tasks realistic, no overbooking, and fit within a normal day.\n"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return {"daily_schedule": response.choices[0].message.content.strip()}

def action_agent(state):
    prompt = (
        f"For each prioritized task below, decide if it needs a reminder "
        f"via Slack, Email, or None. Return only lines like: "
        f"Task - Slack\n\n{state.prioritized_tasks}"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.4
    )
    summary = response.choices[0].message.content.strip()

    for line in summary.splitlines():
        if "Slack" in line:
            send_slack_message(f"🔔 Reminder: {line}")
        elif "Email" in line:
            send_email(subject="Task Reminder", body=line)

    return {"action_summary": summary}
