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
    modified = [resp.replace("ChatGPT", "PlayAI").replace("OpenAI", "Codopia") for resp in server_response]
    response = {"answer": modified}
    return jsonify(response)

if __name__ == "__main__":
    asyncio.run(app.run(host="0.0.0.0", port=5000, debug=True))
