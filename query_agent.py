import streamlit as st
from query_agent import answer_query

# Configure page
st.set_page_config(
    page_title="E-commerce Data Q&A Agent",
    layout="wide",
    initial_sidebar_state="auto",
)
st.title("E-commerce Data Question & Answer Agent")

# User input
query = st.text_input("Ask a question about your e-commerce data:")

if query:
    # Display spinner while LLM and SQL run\    
    with st.spinner("Generating SQL query and answer..."):
        try:
            response = answer_query(query)
        except Exception as e:
            st.error(f"Error: {e}")
        else:
            # Render generated SQL and answer
            st.markdown(response, unsafe_allow_html=True)
