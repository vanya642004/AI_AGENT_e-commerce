import streamlit as st
from db_init import init_db
from query_agent import LlamaSQLAgent
from utils import display_chart

# 1) Page setup
st.set_page_config(page_title="E‑com Data Chatbot", layout="centered")
st.title("📊 E-commerce Data Chatbot")

# 2) Lazy‐load the agent (DB + model) once
@st.cache_resource
def load_agent():
    engine = init_db()
    return LlamaSQLAgent(engine)

# 3) Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "agent" not in st.session_state:
    st.session_state.agent = None

# 4) User input
query = st.text_input("Ask me about your data:")
if query:
    st.session_state.history.append({"role": "user", "content": query})

    # On first query, initialize DB+model
    if st.session_state.agent is None:
        with st.spinner("Loading database and model…"):
            st.session_state.agent = load_agent()

    # Run the agent
    with st.spinner("Thinking…"):
        sql, df = st.session_state.agent.run(query)

    # Record assistant outputs
    st.session_state.history.append({"role": "assistant", "content": f"**SQL**: `{sql}`"})
    st.session_state.history.append({"role": "assistant", "content": df.to_markdown()})
    st.session_state.history.append({"role": "assistant", "content": {"chart": df}})

# 5) Render chat + charts
for msg in st.session_state.history:
    if msg["role"] == "assistant" and isinstance(msg["content"], dict) and "chart" in msg["content"]:
        display_chart(msg["content"]["chart"])
    else:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
