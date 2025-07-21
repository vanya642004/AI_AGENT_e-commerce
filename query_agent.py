import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set your Hugging Face API token directly
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Correct HuggingFaceEndpoint configuration
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",
    model_kwargs={"temperature": 0.7, "max_new_tokens": 512}  # pass inside model_kwargs
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
except Exception as e:
    raise RuntimeError("Agent initialization failed. Check LLM configuration and tool setup.") from e

def answer_query(question: str) -> str:
    try:
        return agent_executor.run(question)
    except Exception as e:
        raise RuntimeError("Query execution failed. Ensure prompt and LLM are correctly aligned.") from e
