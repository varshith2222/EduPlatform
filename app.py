import streamlit as st
from utils.auth import login_form
from utils.layout import tutor_dashboard, student_dashboard

st.set_page_config(page_title="EduPlatform", layout="wide")
st.title("🎓 EduPlatform")

for key in ["logged_in", "role", "username"]:
    if key not in st.session_state: st.session_state[key] = None

if not st.session_state.logged_in:
    role = st.selectbox("Login as", ["Select", "Tutor", "Student"])
    if role != "Select": login_form(role)
else:
    st.sidebar.success(f"Welcome {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = None
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()
    if st.session_state.role == "Tutor": tutor_dashboard()
    elif st.session_state.role == "Student": student_dashboard(st.session_state.username)
