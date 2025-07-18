import streamlit as st
from utils.database import validate_user

def login_form(role):
    st.subheader(f"{role} Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        print(f"🔐 Login button clicked for {role} with username: {username}")
        
        if validate_user(role, username, password):
            print("✅ Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success("Login successful!")
        else:
            print("❌ Login failed — invalid credentials")
            st.error("Invalid username or password.")
