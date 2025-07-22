from flask import Flask, request, jsonify
from db_init import init_db
from query_agent import get_chain

app = Flask(__name__)
# Initialize once
engine = init_db()
chain = get_chain(engine)

@app.route("/query", methods=["POST"])
def query_endpoint():
    payload = request.get_json() or {}
    q = payload.get("query", "")
    answer = chain.run(q)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
