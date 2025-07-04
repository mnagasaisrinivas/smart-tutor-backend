from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    full_name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({"message": "All fields are required."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered."}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(name=full_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)

    response = jsonify({
        "token": access_token,
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
            }
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    response.status_code = 201
    return response


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials."}), 401

    access_token = create_access_token(identity = str(user.id))
    refresh_token = create_refresh_token(identity = str(user.id))

    response = jsonify({
        "token": access_token,
        "user": {"id": user.id, "name": user.name, "email": user.email}
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    response = jsonify({"token": access_token})
    set_access_cookies(response, access_token)
    return response, 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out successfully."})
    unset_jwt_cookies(response)
    return response, 200
