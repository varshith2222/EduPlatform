import streamlit as st
from utils.auth import login_form
from utils.layout import tutor_dashboard, student_dashboard
import os

st.set_page_config(page_title="EduPlatform", layout="wide")
st.title("🎓 EduPlatform")

# Optional debug
DB_URL = os.getenv("FIREBASE_DB_URL")
print("🔥 FIREBASE_DB_URL from app.py:", DB_URL)

# Session state init
for key in ["role_selected", "role", "logged_in", "username"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "role_selected" else False

# Step 1: Role selection
if not st.session_state.role_selected:
    role = st.selectbox("Login as", ["Select", "Tutor", "Student"])
    if role != "Select":
        st.session_state.role = role
        st.session_state.role_selected = True
        st.rerun()

# Step 2: Login
elif not st.session_state.logged_in:
    login_form(st.session_state.role)

# Step 3: Dashboard
else:
    st.sidebar.success(f"Welcome {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        for key in ["role_selected", "role", "logged_in", "username"]:
            st.session_state[key] = None if key != "role_selected" else False
        st.rerun()

    if st.session_state.role == "Tutor":
        tutor_dashboard()
    elif st.session_state.role == "Student":
        student_dashboard(st.session_state.username)
