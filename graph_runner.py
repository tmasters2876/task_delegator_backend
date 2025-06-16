from langgraph.graph import StateGraph, END

# === Agent State ===
class AgentState:
    def __init__(self, raw_input="", daily_context=""):
        self.raw_input = raw_input
        self.classified_tasks = []
        self.optimized_tasks = []
        self.delegated_tasks = []
        self.prioritized_tasks = []
        self.daily_schedule = []
        self.action_summary = ""

    def to_dict(self):
        def safe(obj):
            if hasattr(obj, "model_dump"):
                return obj.model_dump()
            elif hasattr(obj, "__dict__"):
                return obj.__dict__
            elif isinstance(obj, list):
                return [safe(x) for x in obj]
            elif isinstance(obj, dict):
                return {k: safe(v) for k, v in obj.items()}
            else:
                return obj

        return {
            "raw_input": self.raw_input,
            "classified_tasks": safe(self.classified_tasks),
            "optimized_tasks": safe(self.optimized_tasks),
            "delegated_tasks": safe(self.delegated_tasks),
            "prioritized_tasks": safe(self.prioritized_tasks),
            "daily_schedule": safe(self.daily_schedule),
            "action_summary": self.action_summary,
        }

# === Core Task Helpers ===
def classify_tasks(raw_input):
    # Example: very simple stub, adjust to real classifier
    tasks = [task.strip() for task in raw_input.split(",") if task.strip()]
    return [{"task": task} for task in tasks]

def optimize_tasks(tasks):
    # Example: pass-through
    return tasks

def delegate_tasks(tasks):
    # Example: pass-through
    return tasks

def prioritize_tasks(tasks):
    # Example: pass-through
    return tasks

def build_daily_schedule(tasks, daily_context):
    # Example: simple pass-through
    return [{"summary": t.get("task"), "start": "2024-01-01T09:00:00", "end": "2024-01-01T10:00:00"} for t in tasks]

def summarize_action_plan(schedule):
    # Example: count tasks
    return f"Planned {len(schedule)} tasks for today."

# === Graph ===
def build_graph():
    graph = StateGraph(AgentState)

    def classification_agent(state):
        tasks = classify_tasks(state.raw_input)
        state.classified_tasks = tasks
        return state

    def optimization_agent(state):
        optimized = optimize_tasks(state.classified_tasks)
        state.optimized_tasks = optimized
        return state

    def delegation_agent(state):
        delegated = delegate_tasks(state.optimized_tasks)
        state.delegated_tasks = delegated
        return state

    def prioritization_agent(state):
        prioritized = prioritize_tasks(state.delegated_tasks)
        state.prioritized_tasks = prioritized
        return state

    def daily_schedule_agent(state):
        schedule = build_daily_schedule(state.prioritized_tasks, state.daily_context)
        state.daily_schedule = schedule
        return state

    def summarization_agent(state):
        summary = summarize_action_plan(state.daily_schedule)
        state.action_summary = summary
        return state

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

    return graph
