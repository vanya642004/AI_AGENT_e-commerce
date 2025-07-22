```python
import os
import pandas as pd
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent
from langchain_huggingface import HuggingFaceEndpoint

# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize LLM endpoint
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xl",
    temperature=0.7,
)

# Build SQLite DB from CSV files if needed
db_path = "ecommerce.db"
if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    for file in ["data/total_sales.csv", "data/ad_sales.csv", "data/eligibility.csv"]:
        if os.path.exists(file):
            df = pd.read_csv(file)
            table = os.path.splitext(os.path.basename(file))[0].replace(" ", "_").lower()
            df.to_sql(table, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

# Connect LangChain SQL database
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Initialize agent to return intermediate steps
agent_executor = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False,
    return_intermediate_steps=True,
)

# Query handler that shows SQL and answer
def answer_query(question: str) -> str:
    # Execute the agent; this returns a dict including intermediates and output
    result = agent_executor({"input": question})

    # Extract the first SQL snippet from intermediate actions
    sql_snippet = None
    for action, observation in result["intermediate_steps"]:
        if hasattr(action, 'log') and 'SELECT' in action.log.upper():
            sql_snippet = action.log.strip()
            break

    # Prepare display
    sql_display = sql_snippet or "-- Unable to extract SQL --"
    answer_text = result.get("output", "No answer generated.")

    return (
        f"**Generated SQL:**\n```sql\n{sql_display}\n```\n"
        f"**Answer:**\n{answer_text}"
    )
```
