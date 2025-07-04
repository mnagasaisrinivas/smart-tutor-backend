from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.question import Question
from app.utils import get_structured_explanation

ask_bp = Blueprint("ask", __name__)

@ask_bp.route("/", methods=["POST"])
@jwt_required()
def ask_question():
    data = request.get_json()
    subject = data.get("subject")
    question_text = data.get("question")

    if not subject or not question_text:
        return jsonify({"message": "Subject and question are required."}), 400

    try:
        explanation = get_structured_explanation(subject, question_text)
        
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


@ask_bp.route("/save", methods=["POST"])
@jwt_required()
def save_question():
    data = request.get_json()
    subject = data.get("subject")
    question_text = data.get("question")
    answer_steps = data.get("answer_steps")
    answer_summary = data.get("answer_summary")
    user_id = get_jwt_identity()

    if not subject or not question_text or not answer_steps or not answer_summary:
        return jsonify({"message": "Subject, question, answer steps, and answer summary are required."}), 400

    try:
        question = Question(
            user_id=user_id,
            subject=subject,
            question_text=question_text,
            answer_summary=answer_summary
        )
        question.answer_steps_list = answer_steps
        db.session.add(question)
        db.session.commit()
        return jsonify({"message": "Question saved successfully."}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to save question.", "error": str(e)}), 500
    
@ask_bp.route("/saved", methods=["GET"])
@jwt_required()
def get_saved_questions():
    user_id = get_jwt_identity()

    try:
        questions = Question.query.filter_by(user_id=user_id).all()
        return jsonify([
            {
                "id": question.id,
                "subject": question.subject,
                "question_text": question.question_text,
                "answer_steps": question.answer_steps_list,
                "answer_summary": question.answer_summary
            }
            for question in questions
        ]), 200
    
    except Exception as e:
        return jsonify({"message": "Failed to get saved questions.", "error": str(e)}), 500
    

@ask_bp.route("<string:question_id>", methods=["DELETE"])
@jwt_required()
def delete_saved_question(question_id):
    user_id = get_jwt_identity()

    try:
        question = Question.query.filter_by(id=question_id, user_id=user_id).first()
        if not question:
            return jsonify({"message": "Question not found."}), 404
        db.session.delete(question)
        db.session.commit()
        return jsonify({"message": "Question deleted successfully."}), 200
    
    except Exception as e:
        return jsonify({"message": "Failed to delete question.", "error": str(e)}), 500