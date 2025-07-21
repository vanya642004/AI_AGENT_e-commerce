from fastapi import FastAPI
from query_agent import answer_query
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Ensure DB loaded
    from db_init import load_data
    load_data()

@app.get("/ask")
def ask_question(q: str):
    answer = answer_query(q)
    return {"answer": answer}

@app.get("/ask/stream")
def ask_question_stream(q: str):
    answer = answer_query(q)
    def streamer():
        for word in answer.split():
            yield word + " "; time.sleep(0.05)
    return StreamingResponse(streamer(), media_type="text/plain")