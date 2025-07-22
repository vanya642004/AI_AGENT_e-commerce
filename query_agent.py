import os
import pandas as pd
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent
from langchain_huggingface import HuggingFaceEndpoint
from langchain.agents.agent import AgentExecutor

# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ✅ Setup Hugging Face LLM endpoint correctly
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.7  # ✅ Valid argument
)

# ✅ Create SQLite database from CSV if it doesn't exist
if not os.path.exists("ecommerce.db"):
    conn = sqlite3.connect("ecommerce.db")
    csv_files = ["data/total_sales.csv", "data/ad_sales.csv", "data/eligibility.csv"]
    for file in csv_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            table_name = os.path.splitext(os.path.basename(file))[0].replace(" ", "_").lower()
            df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

# ✅ Setup LangChain SQL database
try:
    db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")

# ✅ Initialize SQL agent with parsing error handling
try:
    agent_executor: AgentExecutor = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )
except Exception as e:
    raise RuntimeError("Agent initialization failed. Check LLM and tools.") from e

# ✅ Final query handler with SQL display
def answer_query(question: str) -> str:
    try:
        result = agent_executor.invoke({"input": question})
        sql_generated = ""
        for step in result.get("intermediate_steps", []):
            if "sql_query" in str(step):
                sql_generated = str(step)
                break
        final_output = result.get("output", "No output generated.")
        return f"**Generated SQL:**\n```sql\n{sql_generated}```\n\n**Answer:**\n{final_output}"
    except Exception as e:
        raise RuntimeError("Query execution failed. Ensure prompt and LLM are correctly aligned.") from e
