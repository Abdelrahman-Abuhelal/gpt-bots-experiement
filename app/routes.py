from flask import Blueprint, render_template, request, jsonify
from .models import ChatMessage
from . import db
from openai import OpenAI
import os

main = Blueprint("main", __name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@main.route("/")
def index():
    return render_template("./index.html")


@main.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")

    # Store the question
    new_message = ChatMessage(question=message, response="")
    db.session.add(new_message)
    db.session.commit()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        temperature=0.7,
        max_tokens=64,
        top_p=1,
    )

    if completion.choices and completion.choices[0].message:
        response_content = completion.choices[0].message.content

        new_message.response = response_content
        db.session.commit()

        return response_content
    else:
        return "Failed to Generate response!"


@main.route("/messages", methods=["GET"])
def get_messages():
    messages = ChatMessage.query.all()
    return jsonify(
        [
            {"id": msg.id, "question": msg.question, "response": msg.response}
            for msg in messages
        ]
    )


@main.route("/messages/<int:id>", methods=["GET"])
def get_message(id):
    message = ChatMessage.query.get(id)
    if message:
        return jsonify(
            {
                "id": message.id,
                "question": message.question,
                "response": message.response,
            }
        )
    else:
        return jsonify({"error": "Message not found"}), 404


@main.route("/messages/<int:id>", methods=["PUT"])
def update_message(id):
    message = ChatMessage.query.get(id)
    if message:
        data = request.json
        message.question = data.get("question", message.question)
        message.response = data.get("response", message.response)
        db.session.commit()
        return jsonify(
            {
                "id": message.id,
                "question": message.question,
                "response": message.response,
            }
        )
    else:
        return jsonify({"error": "Message not found"}), 404


@main.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = ChatMessage.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted"})
    else:
        return jsonify({"error": "Message not found"}), 404
