from flask import Flask, request, jsonify
from graph_runner import build_graph, AgentState
from calendar_agent import calendar_agent

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    user_input = data.get("user_input", "")
    daily_context = data.get("daily_context", "")

    # Build agent state
    state = AgentState(raw_input=user_input, daily_context=daily_context)

    # Build and run graph
    graph = build_graph()
    final_state = graph.invoke(state)

    # Run calendar agent
    calendar_result = calendar_agent(final_state)

    # Return all results
    return jsonify({
        "classified_tasks": final_state.classified_tasks,
        "optimized_tasks": final_state.optimized_tasks,
        "delegated_tasks": final_state.delegated_tasks,
        "prioritized_tasks": final_state.prioritized_tasks,
        "daily_schedule": final_state.daily_schedule,
        "action_summary": final_state.action_summary,
        "calendar_confirmation": calendar_result["calendar_confirmation"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
