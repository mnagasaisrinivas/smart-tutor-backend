from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import get_study_notes
from app.models.note import Note
from app.extensions import db

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

        return jsonify({"subject": subject, "topic": topic, "content": content}), 200
    except Exception as e:
        return jsonify({"message": "Failed to generate notes.", "error": str(e)}), 500


@notes_bp.route("/save", methods=["POST"])
@jwt_required()
def save_notes():
    data = request.get_json()
    subject = data.get("subject")
    topic = data.get("topic")
    content = data.get("content")
    heading = content.get("heading")
    bullet_points = content.get("bullet_points", [])
    user_id = get_jwt_identity()

    if not subject or not topic or not content:
        return jsonify({"message": "Subject, topic, and content are required."}), 400

    try:
        note = Note(subject=subject, topic=topic, heading=heading, user_id=user_id)
        note.bullet_points = bullet_points
        db.session.add(note)
        db.session.commit()

        return jsonify({"message": "Note saved successfully."}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to save note.", "error": str(e)}), 500
    

@notes_bp.route("/saved", methods=["GET"])
@jwt_required()
def get_saved_notes():
    user_id = get_jwt_identity()

    try:
        notes = Note.query.filter_by(user_id=user_id).all()
        return jsonify([{
            "id": note.id,
            "subject": note.subject,
            "topic": note.topic,
            "heading": note.heading,
            "bullet_points": note.bullet_points,
            "saved_date": note.saved_date.strftime("%Y-%m-%d %H:%M:%S")
        } for note in notes]), 200
    
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve saved notes.", "error": str(e)}), 500
    

@notes_bp.route("/saved/<string:note_id>", methods=["DELETE"])
@jwt_required()
def delete_saved_note(note_id):
    user_id = get_jwt_identity()

    try:
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return jsonify({"message": "Note not found."}), 404
        db.session.delete(note)
        db.session.commit()

        return jsonify({"message": "Note deleted successfully."}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to delete note.", "error": str(e)}), 500
    

@notes_bp.route("/<string:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()

    try:
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return jsonify({"message": "Note not found."}), 404
        db.session.delete(note)
        db.session.commit()

        return jsonify({"message": "Note deleted successfully."}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to delete note.", "error": str(e)}), 500