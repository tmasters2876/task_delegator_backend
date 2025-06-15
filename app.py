from flask import Flask, request, jsonify
from graph_runner import build_graph, AgentState
from calendar_agent import calendar_agent

import os

app = Flask(__name__)

# ✅ TEMP: One-time JSON uploader
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = file.filename
    save_path = os.path.join("/var/data", filename)
    file.save(save_path)
    return f"✅ Saved {filename} to /var/data.", 200


# ✅ MAIN: Run task flow
@app.route("/run", methods=["POST"])
def run():
    data = request.json
    user_input = data.get("tasks")
    daily_context = data.get("context")

    state = AgentState(raw_input=user_input, daily_context=daily_context)
    graph = build_graph()
    final_state = graph.invoke(state)

    calendar_result = calendar_agent(final_state)

    return jsonify({
        "classified_tasks": final_state["classified_tasks"],
        "optimized_tasks": final_state["optimized_tasks"],
        "delegated_tasks": final_state["delegated_tasks"],
        "prioritized_tasks": final_state["prioritized_tasks"],
        "daily_schedule": final_state["daily_schedule"],
        "action_summary": final_state["action_summary"],
        "calendar_confirmation": calendar_result["calendar_confirmation"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
