import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent

# Set your Hugging Face API token as an environment variable (or via Streamlit Cloud secrets)
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize HuggingFace endpoint model
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    task="text2text-generation",
    temperature=0.0,
    max_length=512
)

# Setup database and agent
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False
)

def answer_query(question: str) -> str:
    return agent_executor.run(question)
