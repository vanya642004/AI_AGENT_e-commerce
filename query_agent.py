import os
import sqlite3
import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint

# Set your Hugging Face API token (ensure HUGGINGFACEHUB_API_TOKEN is set in your env)
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize the HF LLM for SQL generation
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",  # or another compatible HF model
    temperature=0.0
)

# Path to your SQLite database
db_path = "ecommerce.db"


def answer_query(question: str) -> tuple[str, pd.DataFrame]:
    """
    Given a natural language question, generate a single valid SQL query using
    the tables total_sales, ad_sales, and eligibility in ecommerce.db, execute it,
    and return both the SQL string and the resulting DataFrame.
    """
    # 1) Craft prompt for SQL generation
    prompt = (
        "You are an expert SQL generator. "
        "Given a user question and the following SQLite tables: total_sales, ad_sales, eligibility, "
        "generate a single valid SQL query to answer the question. "
        "Only output the SQL query without any explanation.\n\n"
        f"Question: {question}\nSQL:"
    )

    # 2) Call the LLM to get the SQL query
    raw_sql = llm(prompt)
    # Clean up any markdown fences or extra whitespace
    sql = raw_sql.strip().lstrip("```sql").rstrip("```").strip()

    # 3) Execute the query against the SQLite database
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()

    # 4) Return both the SQL and the DataFrame
    return sql, df
