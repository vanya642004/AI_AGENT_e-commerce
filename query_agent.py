# query_agent.py
import os
from db_init import ensure_database
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# 1) Build/reset the DB
ensure_database([
    "data/total_sales.csv",
    "data/ad_sales.csv",
    "data/eligibility.csv",
], db_path="ecommerce.db")

# 2) LLM setup
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.7
)

# 3) SQLDatabase + toolkit
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 4) Agent
agent_executor = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False,
    return_intermediate_steps=True
)

def answer_query(question: str) -> str:
    """
    Returns the generated SQL and the final answer.
    """
    result = agent_executor({"input": question})
    # Extract the SQL from the first intermediate step
    sql_snippet = "-- no SQL generated --"
    for action, _ in result["intermediate_steps"]:
        if hasattr(action, "tool_input") and action.tool_input.strip().upper().startswith("SELECT"):
            sql_snippet = action.tool_input.strip()
            break

    answer = result.get("output", "<no answer>")
    return (
        f"**Generated SQL:**\n```sql\n{sql_snippet}\n```"
        f"\n**Answer:**\n{answer}"
    )
