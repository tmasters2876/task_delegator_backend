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

# === Your classify_tasks, optimize_tasks, delegate_tasks, etc remain unchanged ===

# === Your build_graph() remains unchanged ===
