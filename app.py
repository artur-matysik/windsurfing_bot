import streamlit as st
from src.rag_bot import answer_question

st.set_page_config(page_title="WindBot 🌬️", layout="wide")
st.title("🌊 Windsurfing Bot for Singapore")

# --- Session state setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "log_output" not in st.session_state:
    st.session_state.log_output = []

# --- Live logging ---
def stream_log(msg):
    st.session_state.log_output.append(msg)
    st.session_state.log_output = st.session_state.log_output[-30:]  # keep last 30 lines

# --- Intro ---
st.markdown("""
Ask me anything like:
- *"Is November better than June for windsurfing?"*
- *"Show me wind data near East Coast in March 2024"*
- *"Show daily wind maxima for October 2024 in East Coast. What time during the day they occur?"*
""")

# --- Chat input ---
query = st.chat_input("Type your question here...")
if query:
    with st.spinner("Thinking..."):
        try:
            answer = answer_question(query, log=stream_log)
        except Exception as e:
            answer = f"❌ Error: {e}"

        # Save new chat message
        st.session_state.chat_history.append((query, answer))

        # Immediately display the new one
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            st.markdown(answer)

# --- Display chat history (except most recent, already shown) ---
for q, a in reversed(st.session_state.chat_history[:-1]):
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        st.markdown(a)

# --- Show action log ---
with st.expander("🔧 Action Log", expanded=True):
    for log_line in st.session_state.log_output:
        st.markdown(f"• {log_line}")
