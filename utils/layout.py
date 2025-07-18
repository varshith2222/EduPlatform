import streamlit as st
import time
from utils import database as db

def tutor_dashboard():
    st.title("Tutor Dashboard")
    tabs = st.tabs(["📚 Notes", "📌 Assignments", "📡 Meeting", "❓ Doubts", "🕒 Logs"])

    # 📚 Notes
    with tabs[0]:
        title = st.text_input("Note Title")
        content = st.text_area("Note")
        if st.button("Post Note"):
            db.post_note(title, content)
            st.success("Note posted!")

        notes = db.get_notes()
        for title, note in notes.items():
            st.markdown(f"**{title}**")
            st.write(note["content"])

    # 📌 Assignments
    with tabs[1]:
        title = st.text_input("Assignment Title")
        content = st.text_area("Assignment")
        if st.button("Post Assignment"):
            db.post_assignment(title, content)
            st.success("Assignment posted!")

        assignments = db.get_assignments()
        for title, note in assignments.items():
            st.markdown(f"**{title}**")
            st.write(note["content"])

    # 📡 Meeting
    with tabs[2]:
        link, active = db.get_meeting()

        if not active:
            if st.button("Start Meeting"):
                db.create_meeting()
                db.log_activity("tutor", "Started the meeting")
                st.success("✅ Meeting started!")

                # Open meeting in new tab
                st.markdown(f'''
                    <script>
                    window.open("{db.FIXED_MEET_LINK}", "_blank");
                    </script>
                ''', unsafe_allow_html=True)

                st.experimental_set_query_params(started=str(time.time()))
                st.rerun()
        else:
            st.success("✅ Meeting is currently active")
            if st.button("End Meeting"):
                db.end_meeting()
                db.log_activity("tutor", "Ended the meeting")
                st.warning("🚪 Meeting ended for all participants")

                st.experimental_set_query_params(ended=str(time.time()))
                st.rerun()

    # ❓ Doubts
    with tabs[3]:
        doubts = db.get_doubts()
        for id, d in doubts.items():
            st.markdown(f"**{d['user']} asked:** {d['question']}")
            for ans in d["answers"]:
                st.write(f"💬 {ans}")
            reply = st.text_area(f"Answer to {id}", key=f"ans_{id}")
            image = st.file_uploader("Attach Image (optional)", type=["png", "jpg", "jpeg"], key=f"img_{id}")
            if st.button(f"Reply to {id}", key=f"btn_{id}"):
                answer = reply
                if image:
                    answer += f"\n📎 Image: {image.name} (mocked URL)"
                db.post_answer(id, answer)
                st.success("Answer posted!")

    # 🕒 Logs
    with tabs[4]:
        logs = db.get_all_activities()
        for log in logs.values():
            st.write(f"🕒 {log['timestamp']} — {log['user']}: {log['action']}")


def student_dashboard(username):
    st.title("Student Dashboard")
    tabs = st.tabs(["📚 Notes", "📌 Assignments", "❓ Doubts", "📡 Meeting"])

    # 📚 Notes
    with tabs[0]:
        notes = db.get_notes()
        for title, note in notes.items():
            st.markdown(f"**{title}**")
            st.write(note["content"])
            db.log_activity(username, f"Viewed note: {title}")

    # 📌 Assignments
    with tabs[1]:
        assignments = db.get_assignments()
        for title, note in assignments.items():
            st.markdown(f"**{title}**")
            st.write(note["content"])
            db.log_activity(username, f"Viewed assignment: {title}")

    # ❓ Doubts
    with tabs[2]:
        question = st.text_input("Ask Doubt")
        if st.button("Post Doubt"):
            db.post_doubt(username, question)
            db.log_activity(username, "Posted doubt")

        doubts = db.get_doubts()
        for id, d in doubts.items():
            st.markdown(f"**{d['user']} asked:** {d['question']}")
            for ans in d["answers"]:
                st.write(f"💬 {ans}")
            reply = st.text_input(f"Reply to {id}", key=f"reply_{id}")
            image = st.file_uploader("Attach Image (optional)", type=["png", "jpg", "jpeg"], key=f"img_{id}")
            if st.button(f"Post Answer {id}", key=f"btn_{id}"):
                answer = reply
                if image:
                    answer += f"\n📎 Image: {image.name} (mocked URL)"
                db.post_answer(id, answer)
                st.success("Answer posted!")

    # 📡 Meeting
    with tabs[3]:
        link, active = db.get_meeting()

        if active and link:
            st.success("✅ Live class is in session!")

            if st.button("Join Meeting"):
                db.log_activity(username, "Joined the meeting")
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={link}">', unsafe_allow_html=True)

            # Auto-refresh logic to detect meeting end
            time.sleep(10)
            link, refreshed = db.get_meeting()
            if not refreshed:
                st.warning("🚪 Meeting ended by tutor. You’ve been logged out.")
                for key in ["logged_in", "role_selected", "role", "username"]:
                    st.session_state[key] = None if key != "role_selected" else False
                st.rerun()
            else:
                st.write("🔁 Refreshing to monitor meeting status...")
                st.experimental_set_query_params(last_check=str(time.time()))
                st.rerun()
        else:
            st.info("No active meeting yet.")
