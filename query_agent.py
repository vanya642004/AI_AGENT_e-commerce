import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent
from langchain_huggingface import HuggingFaceEndpoint
from db_init import ensure_database

# 1) Load CSVs into SQLite
csv_files = [
    "data/total_sales.csv",
    "data/ad_sales.csv",
    "data/eligibility.csv",
]
ensure_database(csv_files, db_path="ecommerce.db")

# 2) Init LLM
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.7,
)

# 3) Setup SQL DB & toolkit
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 4) Init agent
agent_executor = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
)

# 5) Query handler

def answer_query(question: str) -> str:
    # agent_executor.invoke returns dict with output & intermediate_steps
    result = agent_executor.invoke({"input": question})
    # get the raw tool input (SQL) from first step
    sql = result["intermediate_steps"][0].tool_input
    answer = result["output"]
    return f"**Generated SQL:**
```sql
{sql}
```
**Answer:** {answer}"
