from flask import Flask, render_template, request, jsonify
from ask import run
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("playai.html")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.form["prompt"]
    # server_response = run(prompt)
    server_response = run(prompt).replace("ChatGPT", "PlayAI").replace("OpenAI", "Codopia")
    response = {"answer": server_response}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2001, debug=True)