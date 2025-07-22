import os
from db_init import ensure_database
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# 1) Load CSVs into SQLite database
csv_files = [
    "total_sales.csv",
    "ad_sales.csv",
    "eligibility.csv",
]
ensure_database(csv_files, db_path="ecommerce.db")

# 2) Initialize LLM endpoint
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.7
)

# 3) Setup SQLDatabase and toolkit
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 4) Initialize agent with intermediate steps
agent_executor = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False,
    return_intermediate_steps=True
)

# 5) Query handler

def answer_query(question: str) -> str:
    """
    Executes the question, extracts the generated SQL, and returns both SQL and answer.
    """
    result = agent_executor({"input": question})
    # Extract SQL from first intermediate step
    sql_snippet = "-- no SQL found --"
    for action, _ in result["intermediate_steps"]:
        if hasattr(action, "tool_input") and action.tool_input.strip().upper().startswith("SELECT"):
            sql_snippet = action.tool_input.strip()
            break

    answer = result.get("output", "<no answer>")
    return (
        f"**Generated SQL:**\n```sql\n{sql_snippet}\n```\n"
        f"**Answer:**\n{answer}"
    )
