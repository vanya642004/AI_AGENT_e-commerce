import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set your HuggingFace token as an environment variable before starting the app
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize the HuggingFace endpoint
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.7,
    max_new_tokens=512
)

# Load CSVs into an in-memory SQLite database
# db_init.py should create `ecommerce.db` by reading your CSV files into tables
from db_init import ensure_database
ensure_database("data/total_sales.csv", "data/ad_sales.csv", "data/eligibility.csv")

db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create an agent that can translate natural language to SQL and run it
agent_executor = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False
)

def answer_query(question: str) -> str:
    """
    Takes a user question, generates the SQL, executes it, and returns:
    1) The generated SQL
    2) The query output
    """
    # Execute the question through the agent
    result = agent_executor.invoke({"input": question})
    # LangChain returns a dict with keys 'output' and 'sql_query'
    sql = result.get("sql_query", "<no SQL generated>")
    output = result.get("output", "<no output>")
    return f"**Generated SQL:**\n```sql\n{sql}\n```\n**Result:**\n{output}"
