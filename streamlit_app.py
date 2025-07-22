import streamlit as st
from query_agent import answer_query

st.set_page_config(page_title="E‑commerce Q&A", layout="wide")
st.title("E‑commerce Data Question & Answer Agent")

query = st.text_input("Ask a question about your e‑commerce data:")

if query:
    with st.spinner("Generating SQL and running it…"):
        try:
            sql, df = answer_query(query)
        except Exception as e:
            st.error(f"❗ Something went wrong:\n{e}")
        else:
            st.markdown("**Generated SQL:**")
            st.code(sql, language="sql")
            st.markdown("**Result:**")
            st.dataframe(df)
