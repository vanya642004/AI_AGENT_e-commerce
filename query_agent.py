import os
import sqlite3
import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint

# Initialize Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Create or connect to the SQLite database (ensure CSVs are loaded)
DB_PATH = "ecommerce.db"

# Initialize the LLM endpoint
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",  # or any compatible HF model
    temperature=0.0,                # deterministic SQL
)


def answer_query(question: str):
    """
    Given a user question, generate a SQL query using the LLM,
    execute it against the ecommerce.db SQLite database, and return
    the SQL string and result DataFrame.
    """
    # 1) Prompt LLM to generate SQL
    prompt = (
        "You are an expert SQL generator for SQLite."
        " Given the tables total_sales, ad_sales, eligibility, "
        "produce a single valid SQL query that answers the user question."
        " Only output the SQL, without explanation.\n"
        f"Question: {question}\nSQL:"
    )
    # Invoke the LLM (raw response)
    raw_sql = llm.invoke([prompt])["generations"][0][0]["text"]

    # 2) Clean up the SQL string
    sql = raw_sql.strip().strip('"').strip('`').strip()

    # 3) Execute against SQLite
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()

    return sql, df
