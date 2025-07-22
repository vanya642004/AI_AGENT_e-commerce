import streamlit as st
import pandas as pd
from db_init import init_db_from_dfs
from query_agent import LlamaSQLAgent
from utils import display_chart

# Page config
st.set_page_config(page_title="CSV Query Agent", layout="centered")
st.title("📊 E-commerce CSV Query Agent")

# Step 1: File uploader
uploaded = st.file_uploader(
    label="Upload CSV files",
    type="csv",
    accept_multiple_files=True
)
if not uploaded:
    st.info("Please upload one or more CSV files to get started.")
    st.stop()

# Step 2: Read uploads into DataFrames
dfs = {f.name: pd.read_csv(f) for f in uploaded}

# Step 3: Initialize DB & Agent (cache so re-run isn't expensive)
@st.cache_resource
def init_agent(dfs_dict):
    engine = init_db_from_dfs(dfs_dict)
    return LlamaSQLAgent(engine)

agent = init_agent(dfs)
# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Step 4: Question input
def handle_query(q: str):
    sql, df = agent.run(q)
    st.session_state.history.append({"role": "assistant", "content": f"**SQL**: `{sql}`"})
    st.session_state.history.append({"role": "assistant", "content": df.to_markdown()})
    st.session_state.history.append({"role": "assistant", "content": {"chart": df}})

query = st.text_input("Ask a question about your data:")
if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.spinner("Processing..."):
        handle_query(query)

# Step 5: Render chat history
for msg in st.session_state.history:
    if msg["role"] == "assistant" and isinstance(msg["content"], dict):
        display_chart(msg["content"]["chart"])
    else:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
