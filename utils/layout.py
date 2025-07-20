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

        for title, note in db.get_notes().items():
            st.markdown(f"**{title}**")
            if isinstance(note, dict) and "content" in note:
                st.write(note["content"])
            else:
                st.write(note)

    # 📌 Assignments
    with tabs[1]:
        title = st.text_input("Assignment Title")
        content = st.text_area("Assignment")
        if st.button("Post Assignment"):
            db.post_assignment(title, content)
            st.success("Assignment posted!")

        for title, note in db.get_assignments().items():
            st.markdown(f"**{title}**")
            if isinstance(note, dict) and "content" in note:
                st.write(note["content"])
            else:
                st.write(note)

    # 📡 Meeting Controls
    with tabs[2]:
        link, active = db.get_meeting()

        if not active:
            if st.button("Start Meeting"):
                db.create_meeting()
                db.log_activity("tutor", "Started the meeting")
                st.success("Meeting started!")

                # 🎥 Reliable button to open Google Meet
                meet_url = db.FIXED_MEET_LINK
                st.markdown(f"""
                    <a href="{meet_url}" target="_blank">
                        <button style='padding:10px;background-color:#4CAF50;border:none;color:white;font-size:16px;cursor:pointer;'>
                            🎥 Enter Google Meet as Host
                        </button>
                    </a>
                """, unsafe_allow_html=True)
        else:
            st.success("Meeting is currently active ✅")
            if st.button("End Meeting"):
                db.end_meeting()
                db.log_activity("tutor", "Ended the meeting")
                st.warning("Meeting ended for all participants")

    # ❓ Doubts
    with tabs[3]:
        for id, d in db.get_doubts().items():
            st.markdown(f"**{d['user']} asked:** {d['question']}")
            for ans in d.get("answers", []):
                st.write(f"💬 {ans}")

            reply = st.text_area(f"Answer to {id}", key=f"ans_{id}")
            image = st.file_uploader("Attach Image (optional)", type=["png", "jpg", "jpeg"], key=f"img_{id}")
            if st.button(f"Reply to {id}", key=f"btn_{id}"):
                answer = reply
                if image:
                    answer += f"\n📎 Image: {image.name} (mocked URL)"
                db.post_answer(id, answer)
                st.success("Answer posted!")

    # 🕒 Activity Logs
    with tabs[4]:
        logs = db.get_all_activities()
        for log in logs.values():
            st.write(f"🕒 {log['timestamp']} — {log['user']}: {log['action']}")


def student_dashboard(username):
    st.title("Student Dashboard")
    tabs = st.tabs(["📚 Notes", "📌 Assignments", "❓ Doubts", "📡 Meeting"])

    # 📚 Notes
    with tabs[0]:
        for title, note in db.get_notes().items():
            st.markdown(f"**{title}**")
            if isinstance(note, dict) and "content" in note:
                st.write(note["content"])
            else:
                st.write(note)
            db.log_activity(username, f"Viewed note: {title}")

    # 📌 Assignments
    with tabs[1]:
        for title, assignment in db.get_assignments().items():
            st.markdown(f"**{title}**")
            if isinstance(assignment, dict) and "content" in assignment:
                st.write(assignment["content"])
            else:
                st.write(assignment)
            db.log_activity(username, f"Viewed assignment: {title}")

    # ❓ Doubts
    with tabs[2]:
        question = st.text_input("Ask Doubt")
        if st.button("Post Doubt"):
            db.post_doubt(username, question)
            db.log_activity(username, "Posted doubt")

        for id, d in db.get_doubts().items():
            st.markdown(f"**{d['user']} asked:** {d['question']}")
            for ans in d.get("answers", []):
                st.write(f"💬 {ans}")

            reply = st.text_input(f"Reply to {id}", key=f"reply_{id}")
            image = st.file_uploader("Attach Image (optional)", type=["png", "jpg", "jpeg"], key=f"img_{id}")
            if st.button(f"Post Answer {id}", key=f"btn_{id}"):
                answer = reply
                if image:
                    answer += f"\n📎 Image: {image.name} (mocked URL)"
                db.post_answer(id, answer)
                st.success("Answer posted!")

    # 📡 Meeting Join
    with tabs[3]:
        link, active = db.get_meeting()
        if active and link:
            st.success("Live class is in session ✅")
            # Styled button-like link
            join_button_html = f"""
            <a href="{link}" target="_blank">
                <button style='padding:10px 20px;background-color:#1f77b4;border:none;color:white;
                               font-size:16px;border-radius:5px;cursor:pointer;'>
                    🎥 Join Google Meet
                </button>
            </a>
            """
            st.markdown(join_button_html, unsafe_allow_html=True)
            db.log_activity(username, "Viewed Join Meeting option")
        else:
            st.info("No active meeting yet.")
