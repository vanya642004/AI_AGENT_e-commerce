import streamlit as st
from query_agent import answer_query

# Configure Streamlit page
st.set_page_config(
    page_title="E-commerce Data Q&A",
    layout="wide"
)
st.title("E-commerce Data Question & Answer Agent")

# User input
query = st.text_input("Ask a question about your e-commerce data:")
if query:
    with st.spinner("Generating SQL & executing..."):
        try:
            sql, df = answer_query(query)
        except Exception as e:
            st.error(f"Error: {e}")
        else:
            st.subheader("Generated SQL Query")
            st.code(sql, language="sql")
            st.subheader("Query Results")
            st.dataframe(df)
