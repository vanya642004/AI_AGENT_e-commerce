import os
import pandas as pd
import sqlite3
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "your_hf_token_here"  # Or set it in environment

# ✅ Fix: Remove 'task', use only supported parameters for HuggingFaceEndpoint
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    model_kwargs={"temperature": 0.7, "max_length": 512}
)

# ✅ Initialize database from CSVs
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

# ✅ Connect LangChain SQL agent to local DB
try:
    db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")

# ✅ Initialize Agent
try:
    agent_executor = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
    )
except Exception as e:
    raise RuntimeError("Agent initialization failed. Check LLM and tools.") from e

# ✅ Main querying function
def answer_query(question: str) -> str:
    try:
        return agent_executor.run(question)
    except Exception as e:
        raise RuntimeError("Query execution failed. Ensure prompt and LLM are correctly aligned.") from e
