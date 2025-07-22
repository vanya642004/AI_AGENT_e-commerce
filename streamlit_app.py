from query_agent import answer_query

# Configure the Streamlit page
st.set_page_config(
    page_title="E-commerce Data Q&A",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Page title
st.title("E-commerce Data Question & Answer Agent")

# User input
query = st.text_import streamlit as st
input("Ask a question about your e-commerce data:")

if query:
    with st.spinner("Generating SQL and fetching results..."):
        try:
            # Generate SQL and execute query
            sql, df = answer_query(query)

            # Display the generated SQL
            st.subheader("Generated SQL Query")
            st.code(sql, language="sql")

            # Display the query results
            st.subheader("Query Results")
            st.dataframe(df)
        except Exception as e:
            # Show any errors that occur
            st.error(f"Error: {e}")
