import streamlit as st
from utils.database import validate_user

def login_form(role):
    st.subheader(f"{role} Login")
    username = st.text_input("Username", key=f"{role}_user")
    password = st.text_input("Password", type="password", key=f"{role}_pass")
    if st.button("Login", key=f"{role}_login"):
        if validate_user(role, username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
