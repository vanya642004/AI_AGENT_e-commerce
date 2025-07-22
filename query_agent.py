import os
from llama_cpp import Llama
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain

class LlamaCppWrapper:
    """
    Wraps llama_cpp.Llama to provide a simple predict interface for LangChain.
    """
    def __init__(self, model_path: str, n_ctx: int = 2048):
        self.client = Llama(model_path=model_path, n_ctx=n_ctx)

    def __call__(self, prompt: str, **kwargs) -> str:
        # Adjust max_tokens or other params as needed
        out = self.client(prompt=prompt, max_tokens=512, **kwargs)
        return out["choices"][0]["text"]

    def predict(self, prompt: str, **kwargs) -> str:
        return self(prompt, **kwargs)


def get_chain(
    engine,
    model_path: str = os.path.join("models", "ggml-model.bin"),
    ctx: int = 2048
):
    # Use our LlamaCpp wrapper instead of langchain.llms.LlamaCpp
    llm = LlamaCppWrapper(model_path=model_path, n_ctx=ctx)
    db = SQLDatabase(engine)
    return SQLDatabaseChain.from_llm(llm, db, verbose=False)
