# 🧠 AI Task Delegator Backend

**Description:**  
This is the Flask API backend for your AI-powered task delegator:
- Classifies, optimizes, delegates, prioritizes tasks
- Sends Slack and Email reminders
- Syncs with Google Calendar

---

## 🚀 How to run locally

```bash
# 1. Create a virtualenv and activate it
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add .env based on .env.example

# 4. Run it!
python app.py

# 5. POST to:
#    http://localhost:8000/run
#    with JSON:
#    {
#      "user_input": "Your tasks...",
#      "daily_context": "Optional notes..."
#    }
