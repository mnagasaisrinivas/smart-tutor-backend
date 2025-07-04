from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.quiz_result import QuizResult
from app.utils.openrouter_api import get_quiz_questions

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate_quiz():
    data = request.get_json()
    subject = data.get("subject")
    topic = data.get("topic")
    if not subject:
        return jsonify({"message": "Subject is required."}), 400

    try:
        questions = get_quiz_questions(subject, topic)
        return jsonify({"subject": subject, "questions": questions}), 200
    except Exception as e:
        return jsonify({"message": "Failed to generate quiz.", "error": str(e)}), 500


@quiz_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_quiz():
    data = request.get_json()
    subject = data.get("subject")
    answers = data.get("answers")  # expects list of selected indices
    questions = data.get("questions")  # expects list of quiz questions with correctAnswer index
    user_id = get_jwt_identity()

    try:
        correct = 0
        for i, question in enumerate(questions):
            if i < len(answers) and answers[i] == question.get("correctAnswer"):
                correct += 1

        score = round((correct / len(questions)) * 100, 2)

        result = QuizResult(
            user_id=user_id,
            subject=subject,
            score=score,
            total_questions=len(questions),
            correct_answers=correct
        )
        db.session.add(result)
        db.session.commit()

        return jsonify({"score": score, "correct": correct, "total": len(questions)}), 200
    except Exception as e:
        return jsonify({"message": "Failed to submit quiz.", "error": str(e)}), 500
