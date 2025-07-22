# streamlit_app.py
import streamlit as st
from query_agent import answer_query
import pandas as pd

# === Page config ===
st.set_page_config(
    page_title="E-commerce Data Q&A",
    layout="wide",
)

st.title("E-commerce Data Question & Answer Agent")
st.write(
    "Ask a natural‑language question about your `total_sales`, `ad_sales`, or `eligibility` tables, "
    "and I'll show you the SQL I'm running and the answers."
)

# === User input ===
query = st.text_input("✏️  Your question:")

if query:
    with st.spinner("⏳ Generating SQL and fetching results..."):
        try:
            sql, df = answer_query(query)
        except Exception as e:
            st.error(f"❗ Something went wrong:\n```\n{e}\n```")
        else:
            st.subheader("🔍 Generated SQL")
            st.code(sql, language="sql")

            if isinstance(df, pd.DataFrame) and not df.empty:
                st.subheader("📊 Query Results")
                st.dataframe(df)
            else:
                st.info("✅ Query ran successfully, but returned no rows.")

