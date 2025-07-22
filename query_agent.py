import os
from llama_cpp import Llama
from langchain.llms import LlamaCpp
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain


def get_chain(
    engine,
    model_path: str = os.path.join("models", "ggml-model.bin"),
    ctx: int = 2048
):
    # Load LLM and build SQL→NL chain
    llm = LlamaCpp(model_path=model_path, n_ctx=ctx)
    db = SQLDatabase(engine)
    return SQLDatabaseChain.from_llm(llm, db, verbose=False)
