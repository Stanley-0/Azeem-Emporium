from uuid import uuid4
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from chatbot import Chatbot


BASE_DIR = Path(__file__).resolve().parent
SITE_DIR = BASE_DIR.parent

app = Flask(__name__, static_folder=str(SITE_DIR), static_url_path="")

# The public site is served from a different domain (GitHub Pages), so only
# that domain may make browser requests to this API.
CORS(app, resources={r"/chat": {"origins": ["https://azeememporium.com"]}})

# Each visitor receives a session id so a multi-step enquiry continues with
# the same handler instead of starting over on every HTTP request.
chatbots = {}


@app.route("/", methods=["GET"])
def home():
    """Serve the Azeem Emporium website."""
    return send_from_directory(SITE_DIR, "index.html")


@app.route("/health", methods=["GET"])
def health():
    """Check whether the chatbot API is running."""
    return jsonify({
        "status": "success",
        "message": "Azeem Emporium chatbot API is running."
    })


@app.route("/chat", methods=["POST"])
def chat():
    """Receive a customer message and return the chatbot response."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "No JSON data was provided."
        }), 400

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "status": "error",
            "message": "Message cannot be empty."
        }), 400

    session_id = data.get("session_id")
    if session_id is not None and not isinstance(session_id, str):
        return jsonify({
            "status": "error",
            "message": "session_id must be a string."
        }), 400

    if not session_id:
        session_id = str(uuid4())

    selected_service = data.get("selected_service", "")
    if not isinstance(selected_service, str):
        return jsonify({
            "status": "error",
            "message": "selected_service must be a string."
        }), 400

    bot = chatbots.get(session_id)
    if bot is None:
        bot = Chatbot()
        chatbots[session_id] = bot
    response = bot.process_message(message, selected_service.strip())

    return jsonify({
        "status": "success",
        "response": response,
        "session_id": session_id
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
