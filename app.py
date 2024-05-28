import asyncio
from flask import Flask, render_template, request, jsonify
from ask import run

app = Flask(__name__)

async def run_async(prompt):
    return await run(prompt)

@app.route("/")
def index():
    return render_template("playai.html")

@app.route("/ask", methods=["POST"])
async def ask():
    prompt = request.form["prompt"]
    server_response = await run_async(prompt)
    server_response = server_response.replace("ChatGPT", "PlayAI").replace("OpenAI", "Codopia")
    response = {"answer": server_response}
    return jsonify(response)

if __name__ == "__main__":
    asyncio.run(app.run(host="0.0.0.0", port=2001, debug=True))
