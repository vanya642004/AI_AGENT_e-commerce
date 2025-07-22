import os
from llama_cpp import Llama
from sqlalchemy import text
import pandas as pd

class LlamaSQLAgent:
    """
    Converts natural-language queries to SQL via Llama.cpp,
    executes against SQLite engine, and returns SQL + DataFrame.
    """
    def __init__(self, engine, model_path: str = os.path.join("models", "ggml-model.bin"), n_ctx: int = 2048):
        self.engine = engine
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)

    def to_sql(self, question: str) -> str:
        prompt = (
            "### Translate the question to SQL for SQLite. "
            "Only output the SQL query without explanation.\n"
            f"Question: {question}\nSQL:"
        )
        resp = self.llm(prompt=prompt, max_tokens=256)
        sql = resp["choices"][0]["text"].strip()
        if not sql.endswith(";"):
            sql += ";"
        return sql

    def run(self, question: str):
        sql = self.to_sql(question)
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return sql, df
