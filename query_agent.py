import os
import sqlite3
import pandas as pd
import glob
from langchain_huggingface import HuggingFaceEndpoint
from db_init import ensure_database

# 1) Load all CSVs in data/ into SQLite database
csv_files = glob.glob("data/*.csv")
ensure_database(csv_files, db_path="ecommerce.db")

# 2) Setup Hugging Face LLM endpoint
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.0
)

# 3) Core query logic: generate SQL, execute it, return both SQL and DataFrame

def answer_query(question: str) -> tuple[str, pd.DataFrame]:
    # Build the prompt for SQL generation
    prompt = (
        "You are an expert SQL generator. "
        "Given a user question, generate exactly one valid SQLite SQL query "
        "using the tables in ecommerce.db (total_sales, ad_sales, eligibility). "
        "Output only the SQL query without explanation.\n"
        f"Question: {question}\n"
        "SQL:"
    )

    # Generate the SQL query via the LLM
    result = llm.generate([prompt])
    sql = result.generations[0][0].text.strip().strip('";')

    # Execute the SQL against the SQLite database
    conn = sqlite3.connect("ecommerce.db")
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()

    return sql, df
