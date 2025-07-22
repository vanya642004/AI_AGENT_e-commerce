import streamlit as st
from db_init import init_db
from query_agent import get_chain
from utils import display_chart

# Page configuration
st.set_page_config(
    page_title="E‑com Data Chatbot",
    layout="centered",
)

st.title("📊 E-commerce Data Chatbot")

# Initialize DB and LLM→SQL chain
engine = init_db()
chain = get_chain(engine)

# Session history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
query = st.text_input("Ask me about your e-commerce data:")
if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.spinner("Processing..."):
        response = chain.run(query)
    st.session_state.history.append({"role": "assistant", "content": response})

# Display chat
for msg in st.session_state.history:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.write(content)
