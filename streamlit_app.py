import streamlit as st
from query_agent import answer_query

# Configure the Streamlit page
st.set_page_config(
    page_title="E-commerce Data Q&A Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("E-commerce Data Question & Answer Agent")

# Input: natural language question
query = st.text_input("Ask a question about your e-commerce data:")

if query:
    with st.spinner("Generating SQL query and retrieving data..."):
        try:
            # Call our query_agent, which returns (sql_string, DataFrame)
            sql, df = answer_query(query)

            # Display the generated SQL
            st.markdown("**Generated SQL:**")
            st.code(sql, language="sql")

            # Display result DataFrame
            st.markdown("**Query Results:**")
            st.dataframe(df)

        except Exception as e:
            st.error(f"Error: {e}")
