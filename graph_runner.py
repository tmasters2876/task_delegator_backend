from langgraph.graph import StateGraph, END
import json

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
            try:
                json.dumps(obj)
                return obj
            except (TypeError, OverflowError):
                if hasattr(obj, "model_dump"):
                    return obj.model_dump()
                elif hasattr(obj, "__dict__"):
                    return {k: safe(v) for k, v in vars(obj).items()}
                elif isinstance(obj, list):
                    return [safe(x) for x in obj]
                elif isinstance(obj, dict):
                    return {k: safe(v) for k, v in obj.items()}
                else:
                    return str(obj)

        return {
            "raw_input": self.raw_input,
            "classified_tasks": safe(self.classified_tasks),
            "optimized_tasks": safe(self.optimized_tasks),
            "delegated_tasks": safe(self.delegated_tasks),
            "prioritized_tasks": safe(self.prioritized_tasks),
            "daily_schedule": safe(self.daily_schedule),
            "action_summary": self.action_summary,
        }

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
    return [{"summary": t["task"], "start": "2024-01-01T09:00:00", "end": "2024-01-01T10:00:00"} for t in tasks]

def summarize_action_plan(schedule):
    return f"Planned {len(schedule)} tasks for today."

def build_graph():
    graph = StateGraph(AgentState)

    def classification_agent(state):
        print("DEBUG: Running classification_agent")
        state.classified_tasks = classify_tasks(state.raw_input)
        return state

    def optimization_agent(state):
        print("DEBUG: Running optimization_agent")
        state.optimized_tasks = optimize_tasks(state.classified_tasks)
        return state

    def delegation_agent(state):
        pprint("DEBUG: Running delegation_agent")
        state.delegated_tasks = delegate_tasks(state.optimized_tasks)
        return state

    def prioritization_agent(state):
        print("DEBUG: Running prioritization_agent")
        state.prioritized_tasks = prioritize_tasks(state.delegated_tasks)
        return state

    def daily_schedule_agent(state):
        print("DEBUG: Running daily_schedule_agent")
        state.daily_schedule = build_daily_schedule(state.prioritized_tasks, state.daily_context)
        return state

    def summarization_agent(state):
        print("DEBUG: Running summarization_agent")
        state.action_summary = summarize_action_plan(state.daily_schedule)
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
