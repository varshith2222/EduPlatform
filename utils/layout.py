import streamlit as st
from utils import database as db

def tutor_dashboard():
    st.title("Tutor Dashboard")
    tabs = st.tabs(["📚 Notes", "📌 Assignments", "📡 Meeting", "❓ Doubts", "🕒 Logs"])

    with tabs[0]:
        title, content = st.text_input("Note Title"), st.text_area("Note")
        if st.button("Post Note"): db.post_note(title, content); st.success("Note posted!")

        notes = db.get_notes()
        for title, note in notes.items():
            st.markdown(f"**{title}**"); st.write(note["content"])

    with tabs[1]:
        title, content = st.text_input("Assignment Title"), st.text_area("Assignment")
        if st.button("Post Assignment"): db.post_assignment(title, content); st.success("Assignment posted!")

        assignments = db.get_assignments()
        for title, note in assignments.items():
            st.markdown(f"**{title}**"); st.write(note["content"])

    with tabs[2]:
        if st.button("Start Meeting"):
            db.create_meeting(); st.success("Meeting started!")
            st.markdown(f'<meta http-equiv="refresh" content="0;URL={db.FIXED_MEET_LINK}">', unsafe_allow_html=True)
        if st.button("End Meeting"):
            db.end_meeting(); st.info("Meeting ended.")

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

    with tabs[4]:
        logs = db.get_all_activities()
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

    with tabs[2]:
        question = st.text_input("Ask Doubt")
        if st.button("Post Doubt"): db.post_doubt(username, question); db.log_activity(username, f"Posted doubt")

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
                db.post_answer(id, answer); st.success("Answer posted!")

    with tabs[3]:
        link, active = db.get_meeting()
        if active and link:
            st.success("Live class is in session!")
            if st.button("Join Meeting"):
                db.log_activity(username, "Joined the meeting")
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={link}">', unsafe_allow_html=True)
        else:
            st.info("No active meeting yet.")
