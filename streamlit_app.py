import streamlit as st
import uuid
from models.chatbot import ChatbotSession

# --------------------------
# Session Initialization
# --------------------------
def start_session():
    session_id = str(uuid.uuid4())
    chatbot = ChatbotSession()
    st.session_state.session_id = session_id
    st.session_state.chatbot = chatbot
    st.session_state.history = []
    st.success(f"✅ Session started: {session_id}")

def ask_question(session_id, question):
    response = st.session_state.chatbot.handle_question(question)
    return response

def end_session(session_id):
    st.success(f"🛑 Session {session_id} ended.")
    del st.session_state.session_id
    del st.session_state.chatbot
    del st.session_state.history

# --------------------------
# First-time setup
# --------------------------
if "session_id" not in st.session_state:
    start_session()

st.title("🧠 Arabic Chatbot Interface")

# Show session ID
st.markdown(f"**Session ID:** `{st.session_state.session_id}`")

# User input
user_input = st.text_input("🧾 اسأل سؤالك:")

# Ask button
if st.button("🔍 إرسال"):
    if user_input.strip():
        response = ask_question(st.session_state.session_id, user_input)
        detailed = response.get("detailed_answer") or response.get("message") or response.get("response")
        st.session_state.history.append((user_input, detailed))
        st.markdown(f"**🤖 الرد:** {detailed}")
    else:
        st.warning("❗️ الرجاء إدخال سؤال.")

# End session button
if st.button("🛑 إنهاء الجلسة"):
    end_session(st.session_state.session_id)
    start_session()

# Show chat history
if st.session_state.get("history"):
    st.markdown("---")
    st.markdown("### 📜 سجل المحادثة")
    for q, r in st.session_state.history:
        st.markdown(f"**أنت**: {q}")
        st.markdown(f"**الرد**: {r}")
