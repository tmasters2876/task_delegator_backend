# graph_runner.py

from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import Optional

from agents import (
    intake_agent,
    classifier_agent,
    optimizer_agent,
    delegator_agent,
    priority_agent,
    planner_agent,
    action_agent
)

class AgentState(BaseModel):
    raw_input: Optional[str] = None
    daily_context: Optional[str] = None
    classified_tasks: Optional[str] = None
    optimized_tasks: Optional[str] = None
    delegated_tasks: Optional[str] = None
    prioritized_tasks: Optional[str] = None
    daily_schedule: Optional[str] = None
    action_summary: Optional[str] = None

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("intake", intake_agent)
    builder.add_node("classifier", classifier_agent)
    builder.add_node("optimizer", optimizer_agent)
    builder.add_node("delegator", delegator_agent)
    builder.add_node("priority", priority_agent)
    builder.add_node("planner", planner_agent)
    builder.add_node("action", action_agent)

    builder.set_entry_point("intake")
    builder.add_edge("intake", "classifier")
    builder.add_edge("classifier", "optimizer")
    builder.add_edge("optimizer", "delegator")
    builder.add_edge("delegator", "priority")
    builder.add_edge("priority", "planner")
    builder.add_edge("planner", "action")

    builder.set_finish_point("action")

    return builder.compile()
