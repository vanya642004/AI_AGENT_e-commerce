import streamlit as st
from query_agent import answer_query

st.set_page_config(
    page_title="E-commerce Data Q&A",
    layout="wide",
)
st.title("E-commerce Data Question & Answer Agent")

query = st.text_input("Ask a question about your e-commerce data:")
if query:
    with st.spinner("Running SQL + LLM..."):
        try:
            response = answer_query(query)
        except Exception as e:
            st.error(e)
        else:
            st.markdown(response, unsafe_allow_html=True)
