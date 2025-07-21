from langchain.llms import HuggingFaceHub
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import initialize_agent
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")  
llm = HuggingFaceHub(
    repo_id="google/flan-t5-xl", model_kwargs={"temperature": 0.0, "max_length": 512}
)

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
