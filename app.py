from flask import Flask, request, jsonify
from graph_runner import build_graph, AgentState
from calendar_agent import calendar_agent
import os

app = Flask(__name__)

UPLOAD_KEY = os.environ.get("ADMIN_UPLOAD_KEY", "mysecretadminkey")
UPLOAD_FOLDER = "/var/data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/run", methods=["POST"])
def run_task_delegator():
    data = request.json or {}
    user_input = data.get("tasks", "")
    daily_context = data.get("daily_context", "")

    state = AgentState(raw_input=user_input, daily_context=daily_context)
    graph = build_graph()
    final_state = graph.invoke(state)

    calendar_result = calendar_agent(final_state)

    # ✅ Use the AgentState's built-in dict conversion
    response = final_state.to_dict()
    response["calendar_confirmation"] = calendar_result["calendar_confirmation"]

    return jsonify(response)

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

@app.route("/", methods=["GET"])
def index():
    return "Task Delegator Backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
