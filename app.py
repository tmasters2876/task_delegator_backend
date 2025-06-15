from flask import Flask, request, jsonify
from graph_runner import build_graph, AgentState
from calendar_agent import calendar_agent
import os

app = Flask(__name__)

# === CONFIG ===
UPLOAD_KEY = os.environ.get("ADMIN_UPLOAD_KEY", "mysecretadminkey")
UPLOAD_FOLDER = "/var/data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === RUN TASK DELEGATOR ===
@app.route("/run", methods=["POST"])
def run_task_delegator():
    data = request.json or {}
    user_input = data.get("tasks", "")
    daily_context = data.get("daily_context", "")

    state = AgentState(raw_input=user_input, daily_context=daily_context)
    graph = build_graph()
    final_state = graph.invoke(state)

    calendar_result = calendar_agent(final_state)

    return jsonify({
        "classified_tasks": final_state.classified_tasks or [],
        "optimized_tasks": final_state.optimized_tasks or [],
        "delegated_tasks": final_state.delegated_tasks or [],
        "prioritized_tasks": final_state.prioritized_tasks or [],
        "daily_schedule": final_state.daily_schedule or [],
        "action_summary": final_state.action_summary or "",
        "calendar_confirmation": (
            calendar_result["calendar_confirmation"]
            if isinstance(calendar_result, dict) and "calendar_confirmation" in calendar_result
            else "No confirmation"
        )
    })

# === UPLOAD SECRETS ===
@app.route("/upload", methods=["POST"])
def upload_secrets():
    auth_header = request.headers.get("Authorization", "")
    if f"Bearer {UPLOAD_KEY}" != auth_header:
        return jsonify({"error": "Unauthorized"}), 403

    if 'credentials' not in request.files or 'token' not in request.files:
        return jsonify({"error": "Missing files"}), 400

    creds_file = request.files['credentials']
    token_file = request.files['token']

    creds_path = os.path.join(UPLOAD_FOLDER, "credentials.json")
    token_path = os.path.join(UPLOAD_FOLDER, "token.json")

    creds_file.save(creds_path)
    token_file.save(token_path)

    return jsonify({"message": "Secrets uploaded successfully."})

# === TEMPORARY: LIST FILES ===
@app.route("/list-files", methods=["GET"])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)})

# === ROOT ===
@app.route("/", methods=["GET"])
def index():
    return "Task Delegator Backend is running."

# === MAIN ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
