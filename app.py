from flask import Flask, request, jsonify
from graph_runner import build_graph, AgentState
from calendar_agent import calendar_agent

app = Flask(__name__)

# Create the LangGraph workflow once
graph = build_graph()

@app.route("/run", methods=["POST"])
def run_task_delegator():
    data = request.get_json()
    user_input = data.get("raw_input", "")
    context = data.get("daily_context", "")

    # Wrap in LangGraph state
    state = AgentState(raw_input=user_input, daily_context=context)

    # Invoke graph
    final_state = graph.invoke(state)

    # Sync Google Calendar
    calendar_result = calendar_agent(final_state)

    return jsonify({
        "classified_tasks": final_state.get("classified_tasks"),
        "optimized_tasks": final_state.get("optimized_tasks"),
        "delegated_tasks": final_state.get("delegated_tasks"),
        "prioritized_tasks": final_state.get("prioritized_tasks"),
        "daily_schedule": final_state.get("daily_schedule"),
        "action_summary": final_state.get("action_summary"),
        "calendar_confirmation": calendar_result["calendar_confirmation"]
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
