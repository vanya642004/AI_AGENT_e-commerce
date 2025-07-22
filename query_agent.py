import os
import sqlite3
import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint

# 1) Load CSVs into SQLite
from db_init import ensure_database
csv_files = ["data/total_sales.csv", "data/ad_sales.csv", "data/eligibility.csv"]
ensure_database(csv_files, db_path="ecommerce.db")

# 2) Setup LLM
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.0
)

# 3) Core query logic: generate SQL, execute it, return both

def answer_query(question: str) -> str:
    # 3a) Prompt to translate to SQL
    prompt = (
        "You are an expert SQL generator. "
        "Given a user question, generate a single valid SQLite SQL query using tables: total_sales, ad_sales, eligibility. "
        "Only output the SQL query, without explanation.
"
        f"Question: {question}
SQL:"
    )
    # call the LLM
    llm_output = llm.generate([prompt])
    # extract generated SQL text
    sql = llm_output.generations[0][0].text.strip().strip('"')

    # 3b) Run the SQL against the DB
    conn = sqlite3.connect("ecommerce.db")
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        conn.close()
        return f"**Generated SQL:**
```sql
{sql}
```
**Error running SQL:** {e}"
    conn.close()

    # 3c) Format output as markdown table
    markdown_table = df.to_markdown(index=False)
    # Combine SQL and results in a single markdown block
    return f"""**Generated SQL:**
```sql
{sql}
```
**Result:**
{markdown_table}
