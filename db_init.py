# query_agent.py
import os
import sqlite3
import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint

# Ensure your HF token is set in the ENV
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize the HF LLM
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.0
)

DB_PATH = "ecommerce.db"

def answer_query(question: str) -> tuple[str, pd.DataFrame]:
    """
    1) Generate a single valid SQL statement for the question.
    2) Run it against ecommerce.db.
    3) Return (sql, DataFrame).
    """
    prompt = (
        "You are an expert SQL generator. "
        "Given this question and tables total_sales, ad_sales, eligibility, "
        "output exactly one valid SQL query (no explanation).\n\n"
        f"Question: {question}\nSQL:"
    )
    raw_sql = llm(prompt)
    sql = (
        raw_sql.replace("```sql", "").replace("```", "").strip()
    )

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()

    return sql, df
