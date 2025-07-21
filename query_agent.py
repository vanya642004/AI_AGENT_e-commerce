import os
import pandas as pd
import sqlite3
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Prompt wrappers for instruction tuning
instruction_prefix = "<s>[INST]"
instruction_suffix = "[/INST]"

def format_prompt(question):
    return f"{instruction_prefix} {question.strip()} {instruction_suffix}"

# Setup HF endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",
    temperature=0.7,
    max_new_tokens=512
)

# Create SQLite database from CSV if it doesn't exist
if not os.path.exists("ecommerce.db"):
    conn = sqlite3.connect("ecommerce.db")
    csv_files = ["total_sales.csv", "ad_sales.csv", "eligibility.csv"]
    for file in csv_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            table_name = os.path.splitext(os.path.basename(file))[0].replace(" ", "_").lower()
            df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

# Setup LangChain SQL database
try:
    db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")

# Initialize SQL agent
try:
    agent_executor = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
    )
except Exception as e:
    raise RuntimeError("Agent initialization failed. Check LLM and tools.") from e

def answer_query(question: str) -> str:
    try:
        prompt = format_prompt(question)
        return agent_executor.run(prompt)
    except Exception as e:
        raise RuntimeError("Query execution failed. Ensure prompt and LLM are correctly aligned.") from e
