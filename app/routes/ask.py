from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.question import Question
from app.utils.openrouter_api import get_structured_explanation, get_study_notes, get_practice_problems, get_quiz_questions

ask_bp = Blueprint("ask", __name__)

@ask_bp.route("/", methods=["POST"])
@jwt_required()
def ask_question():
    data = request.get_json()
    subject = data.get("subject")
    question_text = data.get("question")
    user_id = get_jwt_identity()

    if not subject or not question_text:
        return jsonify({"message": "Subject and question are required."}), 400

    try:
        explanation = get_structured_explanation(subject, question_text)
        # question_entry = Question(
        #     user_id=user_id,
        #     subject=subject,
        #     question_text=question_text,
        #     answer_title = explanation["title"],
        #     answer_steps = "\n".join(f"Step {i+1}: {s}" for i, s in enumerate(explanation.steps)),
        #     answer_summary = explanation["summary"]
        # )
        # db.session.add(question_entry)
        # db.session.commit()

        return jsonify({
            "subject": subject,
            "question": question_text,
            "explanation": {
                "title": explanation["title"],
                "steps": explanation["steps"],
                "summary": explanation["summary"]
            }
        }), 200

    except Exception as e:
        return jsonify({"message": "Failed to get AI explanation.", "error": str(e)}), 500
