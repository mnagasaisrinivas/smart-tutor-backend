from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_practice_problems

practice_bp = Blueprint("practice", __name__)

@practice_bp.route("/", methods=["POST"])
@jwt_required()
def generate_practice():
    data = request.get_json()
    subject = data.get("subject")
    topic = data.get("topic")

    if not subject or not topic:
        return jsonify({"message": "Subject and topic are required."}), 400

    try:
        problems = get_practice_problems(subject, topic)
        return jsonify({"subject": subject, "topic": topic, "problems": problems}), 200
    except Exception as e:
        return jsonify({"message": "Failed to generate practice problems.", "error": str(e)}), 500
