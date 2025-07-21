import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set your Hugging Face API token as an environment variable
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize HuggingFace LLM (pass parameters directly, not via model_kwargs)
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    task="text2text-generation",
    temperature=0.0,
    max_new_tokens=512,
)

# Setup database
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Initialize agent with the SQL toolkit
agent_executor = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
)

def answer_query(question: str) -> str:
    return agent_executor.run(question)

