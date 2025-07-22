import streamlit as st
from streamlit_chat import message
from db_init import init_db
from query_agent import get_chain
from utils import display_chart

# Page config
st.set_page_config(
    page_title="E‑com Data Chatbot",
    layout="centered",
)
st.title("📊 E-commerce Data Chatbot")

# Bootstrap
engine = init_db()
chain = get_chain(engine)
if "history" not in st.session_state:
    st.session_state.history = []

# User input
query = st.text_input("Ask me about your e-commerce data:")
if query:
    st.session_state.history.append((query, True))
    with st.spinner("Processing..."):
        resp = chain.run(query)
    st.session_state.history.append((resp, False))

# Display conversation
for text, is_user in st.session_state.history:
    message(text, is_user=is_user)
