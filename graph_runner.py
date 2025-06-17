from langgraph.graph import StateGraph, END
from notifier import send_slack_reminders, send_email_reminder
from datetime import datetime, timedelta

def classify_tasks(raw_input):
    tasks = [task.strip() for task in raw_input.split(",") if task.strip()]
    return [{"task": task} for task in tasks]

def optimize_tasks(tasks):
    return tasks

def delegate_tasks(tasks):
    return tasks

def prioritize_tasks(tasks):
    return tasks

def build_daily_schedule(tasks, daily_context):
    schedule = []
    # ✅ Use dynamic base time instead of hardcoded date
    base = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    duration = 60  # 1 hr blocks

    for idx, t in enumerate(tasks):
        start_time = base + timedelta(hours=idx)
        end_time = start_time + timedelta(minutes=duration)
        event = {
            "summary": t["task"],
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        }
        schedule.append(event)

    # Slack
    send_slack_reminders(schedule)

    # Email
    email_subject = "Your Daily Schedule"
    email_body = "\n".join([f"{e['summary']} from {e['start']} to {e['end']}" for e in schedule])
    send_email_reminder(email_subject, email_body)

    return schedule

def summarize_action_plan(schedule):
    return f"Planned {len(schedule)} tasks for today."

def build_graph():
    graph = StateGraph(dict)

    def classification_agent(data):
        print("DEBUG: Running classification_agent")
        data["classified_tasks"] = classify_tasks(data["raw_input"])
        return data

    def optimization_agent(data):
        print("DEBUG: Running optimization_agent")
        data["optimized_tasks"] = optimize_tasks(data["classified_tasks"])
        return data

    def delegation_agent(data):
        print("DEBUG: Running delegation_agent")
        data["delegated_tasks"] = delegate_tasks(data["optimized_tasks"])
        return data

    def prioritization_agent(data):
        print("DEBUG: Running prioritization_agent")
        data["prioritized_tasks"] = prioritize_tasks(data["delegated_tasks"])
        return data

    def daily_schedule_agent(data):
        print("DEBUG: Running daily_schedule_agent")
        data["daily_schedule"] = build_daily_schedule(data["prioritized_tasks"], data["daily_context"])
        return data

    def summarization_agent(data):
        print("DEBUG: Running summarization_agent")
        data["action_summary"] = summarize_action_plan(data["daily_schedule"])
        return data

    graph.add_node("classify", classification_agent)
    graph.add_node("optimize", optimization_agent)
    graph.add_node("delegate", delegation_agent)
    graph.add_node("prioritize", prioritization_agent)
    graph.add_node("schedule", daily_schedule_agent)
    graph.add_node("summarize", summarization_agent)

    graph.set_entry_point("classify")
    graph.add_edge("classify", "optimize")
    graph.add_edge("optimize", "delegate")
    graph.add_edge("delegate", "prioritize")
    graph.add_edge("prioritize", "schedule")
    graph.add_edge("schedule", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()
