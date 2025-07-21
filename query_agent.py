import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set your Hugging Face API token as an environment variable
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Use chat-compatible model
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    model_kwargs={"temperature": 0.7, "max_new_tokens": 512},
)

# Setup database
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Prompt template for direct SQL-powered QA
template = """Use the SQL database to answer the question:
{question}"""
prompt = PromptTemplate(input_variables=["question"], template=template)

# Create LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

def answer_query(question: str) -> str:
    return chain.run(question)
