from flask import request, jsonify
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.audit_log import AuditLog
from flask_jwt_extended import create_access_token

def register():
    data = request.get_json()

    # Validate required fields
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Name, email and password are required"}), 400

    # Check if user already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    # Hash password
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_pw,
        role=data.get("role", "viewer")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201


def login():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is inactive"}), 403

    token = create_access_token(identity=user.id)

    # Log the action
    log = AuditLog(user_id=user.id, action="User logged in")
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": "Login successful",
        "token": token,
        "role": user.role
    }), 200