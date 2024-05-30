from flask import Flask, render_template, request, jsonify
import asyncio
from ask import run

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("playai.html")

@app.route("/ask", methods=["POST"])
async def ask():
    prompt = request.form["prompt"]
    server_response = await run(prompt)
    response = {"answer": server_response}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
