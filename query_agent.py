# query_agent.py
import os
import sqlite3
import pandas as pd
import glob
from langchain_huggingface import HuggingFaceEndpoint
from db_init import ensure_database

# 1) Load all CSVs in data/ into SQLite
csv_files = glob.glob("data/*.csv")
ensure_database(csv_files, db_path="ecommerce.db")

# 2) Setup LLM
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.0
)

def answer_query(question: str) -> str:
    # 3a) Prompt to translate to SQL
    prompt = (
        "You are an expert SQL generator. "
        "Generate exactly one valid SQLite SQL query using the tables in ecommerce.db. "
        "Output only the SQL query without any explanation.\n"
        f"Question: {question}\n"
        "SQL:"
    )
    llm_result = llm.generate([prompt])
    sql = llm_result.generations[0][0].text.strip().strip('"')

    # 3b) Execute the SQL
    conn = sqlite3.connect("ecommerce.db")
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as exec_err:
        conn.close()
        return (
            f"**Generated SQL:**\n```sql\n{sql}\n```\n"
            f"**Error running SQL:** {exec_err}"
        )
    conn.close()

    # 3c) Render results as Markdown table
    table_md = df.to_markdown(index=False)
    return (
        f"**Generated SQL:**\n```sql\n{sql}\n```\n\n"
        f"**Result:**\n{table_md}"
    )
