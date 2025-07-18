import streamlit as st
from utils.auth import get_authenticator
from utils.layout import tutor_dashboard, student_dashboard
import os

# 🔧 Optional debug: Show Firebase URL
DB_URL = os.getenv("FIREBASE_DB_URL")
print("🔥 FIREBASE_DB_URL from app.py:", DB_URL)

# 🎓 UI config
st.set_page_config(page_title="EduPlatform", layout="wide")
st.title("🎓 EduPlatform")

# 🚀 Init session state
for key, default in {
    "role_selected": False,
    "role": None,
    "authenticator": None,
    "auth_status": None,
    "username": None,
    "name": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# 🔑 Step 1: Role Selection
if not st.session_state.role_selected:
    role = st.selectbox("Login as", ["Tutor", "Student"])
    if role != "Select":
        st.session_state.role = role
        st.session_state.role_selected = True
        st.rerun()

# 🔐 Step 2: Login
if st.session_state.role_selected and st.session_state.auth_status is None:
    st.subheader(f"{st.session_state.role} Login")

    # Get authenticator for selected role
    st.session_state.authenticator = get_authenticator(st.session_state.role)
    name, auth_status, username = st.session_state.authenticator.login("Login", "main")

    if auth_status is not None:
        st.session_state.auth_status = auth_status
        st.session_state.username = username
        st.session_state.name = name
        st.rerun()

# 🧭 Step 3: Dashboard
if st.session_state.auth_status is True:
    st.session_state.authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {st.session_state.name}!")

    # Load role-specific dashboard
    if st.session_state.role == "Tutor" and st.session_state.username == "tutor":
        tutor_dashboard()
    elif st.session_state.role == "Student" and st.session_state.username.startswith("student"):
        student_dashboard(st.session_state.username)
