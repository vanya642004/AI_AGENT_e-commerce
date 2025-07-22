import streamlit as st
from sqlalchemy import text
from db_init import init_db
from query_agent import LlamaSQLAgent
from utils import display_chart

# Page setup
st.set_page_config(page_title="E‑com Data Chatbot", layout="centered")
st.title("📊 E-commerce Data Chatbot")

# Init
engine = init_db()
agent = LlamaSQLAgent(engine)

# History
if "history" not in st.session_state:
    st.session_state.history = []

# Input
query = st.text_input("Ask me about your data:")
if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.spinner("Thinking..."):
        sql, df = agent.run(query)
    # Record assistant turn
    st.session_state.history.append({"role": "assistant", "content": f"SQL: `{sql}`"})
    st.session_state.history.append({"role": "assistant", "content": df.to_markdown()})
    # Chart if numeric
    st.session_state.history.append({"role": "assistant", "content": {"chart": df}})

# Display
for msg in st.session_state.history:
    if msg["role"] == "assistant" and isinstance(msg["content"], dict) and "chart" in msg["content"]:
        display_chart(msg["content"]["chart"])
    else:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
