import os
import pandas as pd
import sqlite3
from langchain_community.llms import HuggingFaceHub
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set your HF token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Use a supported Hugging Face Hub model (must support `__call__`)
llm = HuggingFaceHub(
    repo_id="google/flan-t5-xl",
    model_kwargs={"temperature": 0.7, "max_length": 512}
)

# Build SQLite DB from uploaded CSVs
if not os.path.exists("ecommerce.db"):
    conn = sqlite3.connect("ecommerce.db")
    csv_files = [
        ("data/total_sales.csv", "total_sales"),
        ("data/ad_sales.csv", "ad_sales"),
        ("data/eligibility.csv", "eligibility")
    ]
    for file_path, table_name in csv_files:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

# Load DB using LangChain
try:
    db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")

# Initialize agent
try:
    agent_executor = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )
except Exception as e:
    raise RuntimeError("Agent initialization failed. Check LLM and tools.") from e

# Main answer function
def answer_query(question: str) -> str:
    try:
        return agent_executor.run(question)
    except Exception as e:
        raise RuntimeError("Query execution failed. Ensure prompt and LLM are correctly aligned.") from e
