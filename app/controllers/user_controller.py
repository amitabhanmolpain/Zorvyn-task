from flask import request, jsonify
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.audit_log import AuditLog
from flask_jwt_extended import get_jwt_identity

def get_all_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role": u.role,
        "is_active": u.is_active
    } for u in users]), 200


def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }), 200


def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    current_user_id = get_jwt_identity()

    if "name" in data:
        user.name = data["name"]
    if "role" in data:
        if data["role"] not in ["viewer", "analyst", "admin"]:
            return jsonify({"error": "Invalid role"}), 400
        user.role = data["role"]
    if "is_active" in data:
        user.is_active = data["is_active"]

    # Log the action
    log = AuditLog(user_id=current_user_id, action=f"Updated user {user_id}")
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    current_user_id = get_jwt_identity()

    # Log before delete
    log = AuditLog(user_id=current_user_id, action=f"Deleted user {user_id}")
    db.session.add(log)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200