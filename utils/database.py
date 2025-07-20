import requests, os
from dotenv import load_dotenv
from datetime import datetime

# 🔧 Load environment variables
load_dotenv()
DB_URL = os.getenv("FIREBASE_DB_URL")
if not DB_URL:
    raise ValueError("❌ FIREBASE_DB_URL is not set!")
DB_URL = DB_URL.rstrip("/")

# 🔍 Print Firebase URL for Render logs
print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
print("🔥 Firebase DB URL:", DB_URL)
print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")

# 🔗 Fixed meeting link
FIXED_MEET_LINK = "http://meet.google.com/huq-xcht-qcb"

# 🔧 Firebase GET
def _get(path):
    try:
        response = requests.get(f"{DB_URL}/{path}.json")
        print(f"📡 GET {path} → {response.status_code}")
        return response.json() or {}
    except Exception as e:
        print(f"❌ GET error for {path}:", e)
        return {}

# 🔧 Firebase PUT
def _put(path, data):
    try:
        response = requests.put(f"{DB_URL}/{path}.json", json=data)
        print(f"📡 PUT {path} → {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ PUT error for {path}:", e)
        return None

# 🔧 Firebase POST
def _post(path, data):
    try:
        response = requests.post(f"{DB_URL}/{path}.json", json=data)
        print(f"📡 POST {path} → {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ POST error for {path}:", e)
        return None

# 🔐 Validate user login
def validate_user(role, username, password):
    users = _get(f"users/{role.lower()}s")
    print(f"🧪 Role: {role}, Username: {username}, Password: {password}")
    print("🧪 Fetched users:", users)
    actual_password = users.get(username, {}).get("password")
    print("🧪 Actual password from DB:", actual_password)
    return actual_password == password

# 📝 Notes
def post_note(title, content):
    _put(f"notes/{title}", {"content": content})

def get_notes():
    return _get("notes")

# 📚 Assignments
def post_assignment(title, content):
    _put(f"assignments/{title}", {"content": content})

def get_assignments():
    return _get("assignments")

# ❓ Doubts
def post_doubt(user, question):
    _post("doubts", {"user": user, "question": question, "answers": []})

def post_answer(doubt_id, answer):
    doubt = _get(f"doubts/{doubt_id}")
    if doubt:
        doubt["answers"].append(answer)
        _put(f"doubts/{doubt_id}", doubt)

def get_doubts():
    return _get("doubts")

# 📅 Meeting
def create_meeting():
    _put("meeting/current", {"link": FIXED_MEET_LINK, "active": True})

def end_meeting():
    _put("meeting/current/active", False)

def get_meeting():
    data = _get("meeting/current")
    return data.get("link"), data.get("active", False) if isinstance(data, dict) else (None, False)

# 🕵️ Activity Logs
def log_activity(user, action):
    _post("activity_logs", {
        "user": user,
        "action": action,
        "timestamp": datetime.utcnow().isoformat()
    })

def get_all_activities():
    return _get("activity_logs")
