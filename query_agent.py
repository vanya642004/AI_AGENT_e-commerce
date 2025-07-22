import os
import sqlite3
import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint

# Load your HF token however you prefer; here we pull from ENV
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

DB_PATH = "ecommerce.db"

# 1) Initialize your LLM
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.0,   # deterministic SQL generation
)

def answer_query(question: str):
    """
    1) Ask the LLM to generate a single valid SQLite SQL query.
    2) Run that query against ecommerce.db.
    3) Return the SQL string and the pandas DataFrame.
    """
    prompt = (
        "You are an expert SQL generator for SQLite. "
        "Given tables total_sales, ad_sales, eligibility, write a single valid SQL query answering the user. "
        "Output ONLY the SQL (no explanation).\n"
        f"Question: {question}\nSQL:"
    )
    # invoke() returns a dict with generations
    out = llm.invoke([prompt])
    raw_sql = out["generations"][0][0]["text"]
    sql = raw_sql.strip().strip("`").strip('"')

    # execute
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()

    return sql, df
