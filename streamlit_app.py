import streamlit as st
from query_agent import answer_query

st.set_page_config(page_title="E-commerce Chat Agent")
st.title("E-commerce Data Question and Answer Agent")

query = st.text_input("Ask a question about your e-commerce data:")
if query:
    with st.spinner("Generating answer..."):
        answer = answer_query(query)
    st.markdown("Answer:")
    st.write(answer)