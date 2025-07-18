import requests, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DB_URL = os.getenv("FIREBASE_DB_URL").rstrip("/")
print("🔥 Firebase DB URL:", DB_URL)
FIXED_MEET_LINK = "https://meet.google.com/abc-defg-hij"

def _get(path):
    try: return requests.get(f"{DB_URL}/{path}.json").json() or {}
    except: return {}

def _put(path, data):
    try: return requests.put(f"{DB_URL}/{path}.json", json=data)
    except: return None

def _post(path, data):
    try: return requests.post(f"{DB_URL}/{path}.json", json=data)
    except: return None

def validate_user(role, username, password):
    users = _get(f"users/{role.lower()}s")
    return users.get(username, {}).get("password") == password

def post_note(title, content): _put(f"notes/{title}", {"content": content})
def get_notes(): return _get("notes")

def post_assignment(title, content): _put(f"assignments/{title}", {"content": content})
def get_assignments(): return _get("assignments")

def post_doubt(user, question): _post("doubts", {"user": user, "question": question, "answers": []})
def post_answer(doubt_id, answer):
    doubt = _get(f"doubts/{doubt_id}")
    if doubt: doubt["answers"].append(answer); _put(f"doubts/{doubt_id}", doubt)
def get_doubts(): return _get("doubts")

def create_meeting(): _put("meeting/current", {"link": FIXED_MEET_LINK, "active": True})
def end_meeting(): _put("meeting/current/active", False)
def get_meeting():
    data = _get("meeting/current")
    return data.get("link"), data.get("active", False) if isinstance(data, dict) else (None, False)

def log_activity(user, action):
    _post("activity_logs", {
        "user": user,
        "action": action,
        "timestamp": datetime.utcnow().isoformat()
    })
def get_all_activities(): return _get("activity_logs")
