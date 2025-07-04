from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.openrouter_api import get_study_notes

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/", methods=["POST"])
@jwt_required()
def generate_notes():
    data = request.get_json()
    subject = data.get("subject")
    topic = data.get("topic")
    user_id = get_jwt_identity()

    if not subject or not topic:
        return jsonify({"message": "Subject and topic are required."}), 400

    try:
        content = get_study_notes(subject, topic)
        # note = Note(user_id=user_id, subject=subject, topic=topic, content=content)
        # db.session.add(note)
        # db.session.commit()

        return jsonify({"subject": subject, "topic": topic, "content": content}), 200
    except Exception as e:
        return jsonify({"message": "Failed to generate notes.", "error": str(e)}), 500
