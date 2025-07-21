import os
from langchain_community.llms import HuggingFaceHub
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set your Hugging Face API token directly or from environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # Assumes token is set in Streamlit secrets or env

# Correct HuggingFaceHub initialization (public model usage)
llm = HuggingFaceHub(
    repo_id="google/flan-t5-xl",
    model_kwargs={"temperature": 0.0, "max_new_tokens": 512}
)

# Setup database
try:
    db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")

# Initialize agent with the SQL toolkit
try:
    agent_executor = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
    )
except AttributeError as e:
    raise AttributeError("Agent initialization failed. Likely LLM misconfiguration.") from e

def answer_query(question: str) -> str:
    try:
        return agent_executor.run(question)
    except AttributeError as e:
        raise AttributeError("Query execution failed due to misconfigured agent or inputs.") from e
