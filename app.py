import streamlit as st
import requests, os

DB_URL = os.getenv("FIREBASE_DB_URL").rstrip("/")
print("🔥 Firebase DB URL:", DB_URL)

def _get(path):
    try:
        response = requests.get(f"{DB_URL}/{path}.json")
        print(f"📡 GET {path} → {response.status_code}")
        return response.json() or {}
    except Exception as e:
        print(f"❌ GET error for {path}:", e)
        return {}

def validate_user(role, username, password):
    users = _get(f"users/{role.lower()}s")
    print(f"🧪 Role: {role}, Username: {username}, Password: {password}")
    print("🧪 Fetched users:", users)
    actual_password = users.get(username, {}).get("password")
    print("🧪 Actual password from DB:", actual_password)
    return actual_password == password

st.title("🧪 Login Test")

role = st.selectbox("Role", ["Student", "Tutor"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if validate_user(role, username, password):
        st.success("✅ Login successful!")
    else:
        st.error("❌ Invalid username or password.")
