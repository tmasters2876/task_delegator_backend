from langgraph.graph import StateGraph, END
from graph_runner import (
    classify_tasks,
    optimize_tasks,
    delegate_tasks,
    prioritize_tasks,
    build_daily_schedule,
    summarize_action_plan,
    AgentState,
    build_graph
)

# === Core Task Agents ===
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

# === Graph ===
def build_agent_graph():
    graph = StateGraph(AgentState)

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
