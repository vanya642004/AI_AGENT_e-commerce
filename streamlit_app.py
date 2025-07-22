import streamlit as st
from query_agent import answer_query

st.set_page_config(
    page_title="E-commerce Data Q&A",
    layout="wide"
)
st.title("E-commerce Data Question & Answer Agent")

query = st.text_input("Ask a question about your e-commerce data:")
if query:
    with st.spinner("Generating SQL & running it…"):
        try:
            result_md = answer_query(query)
            st.markdown(result_md, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Something went wrong: {e}")


