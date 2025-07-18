import streamlit as st
from utils import database as db

def tutor_dashboard():
    st.title("Tutor Dashboard")
    tabs = st.tabs(["📚 Notes", "📌 Assignments", "📡 Meeting"])
    with tabs[0]:
        title, content = st.text_input("Note Title"), st.text_area("Note")
        if st.button("Post Note"): db.post_note(title, content); st.success("Note posted!")
    with tabs[1]:
        title, content = st.text_input("Assignment Title"), st.text_area("Assignment")
        if st.button("Post Assignment"): db.post_assignment(title, content); st.success("Assignment posted!")
    with tabs[2]:
        link, active = db.get_meeting()

        if not active:
            if st.button("Start Meeting"):
                db.create_meeting()
                db.log_activity("tutor", "Started the meeting")
                st.success("Meeting started!")

                # 🔗 Open Meet in a new tab
                st.markdown(f"""
                    <script>
                    window.open("{db.FIXED_MEET_LINK}", "_blank");
                    </script>
                """, unsafe_allow_html=True)

        else:
            st.success("Meeting is active ✅")
            if st.button("End Meeting"):
                db.end_meeting()
                db.log_activity("tutor", "Ended the meeting")
                st.warning("Meeting ended.")
    
        # 📋 Student Activity Logs
        logs = db.get_all_activities()
        st.subheader("Student Activity Logs")
        for log in logs.values():
            st.write(f"🕒 {log['timestamp']} — {log['user']}: {log['action']}")

def student_dashboard(username):
    st.title("Student Dashboard")
    tabs = st.tabs(["📚 Notes", "📌 Assignments", "❓ Doubts", "📡 Meeting"])
    with tabs[0]:
        for title, note in db.get_notes().items():
            st.markdown(f"**{title}**"); st.write(note["content"])
            db.log_activity(username, f"Viewed note: {title}")
    with tabs[1]:
        for title, assignment in db.get_assignments().items():
            st.markdown(f"**{title}**"); st.write(assignment["content"])
            db.log_activity(username, f"Viewed assignment: {title}")
    with tabs[3]:
        link, active = db.get_meeting()
        if active and link:
            st.success("Live class is in session ✅")
            if st.button("Join Meeting"):
                db.log_activity(username, "Joined the meeting")
                st.markdown(f"""
                    <script>
                    window.open("{link}", "_blank");
                    </script>
                """, unsafe_allow_html=True)
        else:
            st.info("No active meeting yet.")
    with tabs[3]:
        link, active = db.get_meeting()
        if active and link:
            st.success("Live class is in session!")
            if st.button("Join Meeting"):
                db.log_activity(username, "Joined the meeting")
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={link}">', unsafe_allow_html=True)
        else:
            st.info("No active meeting yet.")
