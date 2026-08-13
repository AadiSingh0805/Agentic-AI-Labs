import streamlit as st
import pandas as pd
from Labs.DeterministicLLMTutor.tutor_agent import DeterministicDSTutor
from Labs.DeterministicLLMTutor.logger import fetch_logs

st.set_page_config(page_title="Deterministic DSTutor", page_icon="🎓", layout="wide")

st.title("🎓 DeterministicDSTutor")
st.markdown("A deterministic, rule-based tutoring agent leveraging optimized prompts and intent classification.")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Agent
@st.cache_resource
def load_agent():
    return DeterministicDSTutor()

agent = load_agent()

# Sidebar - Audit Logs & System Status
with st.sidebar:
    st.header("📊 Audit Logs")
    
    if not agent.api_available:
        st.error("⚠️ Gemini API Key Missing or Invalid.")
    else:
        st.success("⚡ Gemini API Connected [Temp=0]")

    st.markdown("---")
    if st.button("Refresh Logs"):
        st.rerun()

    logs = fetch_logs(limit=20)
    if logs:
        df_logs = pd.DataFrame(logs, columns=[
            "Time", "Question", "Topic", "Objective", "Latency (ms)", "Response"
        ])
        st.dataframe(df_logs[["Time", "Question", "Topic", "Objective", "Latency (ms)"]], use_container_width=True)
    else:
        st.info("No interactions logged yet.")

# Main Interface: Chat Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "metadata" in msg:
            m = msg["metadata"]
            st.caption(
                f"🎯 **Topic:** `{m['intent']}` | 🔍 **Objective:** `{m['subintent']}` | "
                f"⚡ **Latency:** `{m['latency_ms']} ms` | 💾 **Cached:** `{m['cached']}`"
            )

# Chat Input - Updated placeholder to match the new Core Data Science JSON
user_input = st.chat_input("Ask a Data Science question (e.g., 'What is EDA?', 'Show me code for Data Wrangling')")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Corrected: Only pass the user_input, no history argument
    result = agent.answer_query(user_input)
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "metadata": {
            "intent": result["intent"],
            "subintent": result["subintent"],
            "latency_ms": result["latency_ms"],
            "cached": result["cached"]
        }
    })
    
    st.rerun()