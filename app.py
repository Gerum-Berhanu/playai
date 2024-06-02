from flask import Flask, render_template, request, jsonify
import asyncio
import threading
from ask import run, init_browser, close_browser

app = Flask(__name__)

# Create and set a new event loop in a separate thread
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Start the event loop in a new thread
loop_thread = threading.Thread(target=start_loop, args=(loop,))
loop_thread.start()

# Initialize the browser in the background loop
asyncio.run_coroutine_threadsafe(init_browser(), loop)

@app.route("/")
def index():
    return render_template("playai.html")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.form["prompt"]
    future = asyncio.run_coroutine_threadsafe(run(prompt), loop)
    server_response = future.result()
    response = {"answer": server_response}
    return jsonify(response)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        future = asyncio.run_coroutine_threadsafe(close_browser(), loop)
        future.result()
        loop.stop()
        loop_thread.join()
