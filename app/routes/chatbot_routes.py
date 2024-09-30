# chatbot_routes

from flask import Blueprint, request, jsonify, render_template
from ..services.chatbot_service import (
    process_chatbot1,
    process_chatbot2,
    process_chatbot3,
    create_chat_model,
)

main = Blueprint("chatbot", __name__)


@main.route("/")
def index():
    return render_template("./index.html")


@main.route("/api/<chatbot_id>", methods=["POST"])
def chatbot_api(chatbot_id):
    """Main API handler for chatbot requests."""
    question = request.json.get("message")

    if not question:
        return jsonify({"error": "Message is required"}), 400

    llm = create_chat_model()

    if chatbot_id == "chatbot1":
        return jsonify(process_chatbot1(llm, question, chatbot_id))
    elif chatbot_id == "chatbot2":
        return jsonify(process_chatbot2(llm, question, chatbot_id))
    elif chatbot_id == "chatbot3":
        return jsonify(process_chatbot3(llm, question, chatbot_id))
    else:
        return jsonify({"error": "Invalid chatbot ID"}), 404
