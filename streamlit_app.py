# streamlit_app.py
import streamlit as st
from models.chatbot import ChatbotSession
import uuid

# Simple session store in Streamlit (per-user)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatbotSession()

st.title("🧠 Chatbot UI")

st.markdown("**Session ID**: " + st.session_state.session_id)

query = st.text_input("Enter your question:")

if st.button("Send"):
    if query.strip():
        response = st.session_state.chat_session.handle_question(query)
        st.markdown(f"**Bot:** {response['response']}")
    else:
        st.warning("Please enter a question.")

if st.button("End Session"):
    st.session_state.chat_session = ChatbotSession()
    st.session_state.session_id = str(uuid.uuid4())
    st.success("Session restarted.")

# Optional: Show history
st.markdown("---")
st.markdown("### Conversation History")
for i, (q, r) in enumerate(st.session_state.chat_session.history):
    st.markdown(f"**You**: {q}")
    st.markdown(f"**Bot**: {r}")
