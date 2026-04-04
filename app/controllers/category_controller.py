from flask import request, jsonify
from app.extensions import db
from app.models.category import Category
from app.models.audit_log import AuditLog
from flask_jwt_extended import get_jwt_identity


def get_all_categories():
    categories = Category.query.all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name
        } for c in categories
    ]), 200


def create_category():
    data = request.get_json()
    current_user_id = int(get_jwt_identity())

    if not data or not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    existing = Category.query.filter_by(name=data["name"]).first()
    if existing:
        return jsonify({"error": "Category already exists"}), 409

    category = Category(name=data["name"])
    db.session.add(category)

    log = AuditLog(user_id=current_user_id, action=f"Created category {data['name']}")
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Category created successfully", "category_id": category.id}), 201


def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    current_user_id = int(get_jwt_identity())
    category_name = category.name

    db.session.delete(category)

    log = AuditLog(user_id=current_user_id, action=f"Deleted category {category_name}")
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"}), 200