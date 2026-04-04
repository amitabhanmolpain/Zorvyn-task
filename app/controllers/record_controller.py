from flask import request, jsonify
from app.extensions import db
from app.models.financial_record import FinancialRecord
from app.models.audit_log import AuditLog
from app.models.category import Category
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from sqlalchemy.exc import IntegrityError

def get_all_records():
    query = FinancialRecord.query.filter_by(is_deleted=False)

    # Filters
    record_type = request.args.get("type")
    category_id = request.args.get("category_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if record_type:
        query = query.filter_by(type=record_type)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if start_date:
        query = query.filter(FinancialRecord.date >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(FinancialRecord.date <= datetime.strptime(end_date, "%Y-%m-%d"))

    search = request.args.get("search")
    if search:
        query = query.filter(FinancialRecord.notes.ilike(f"%{search}%"))

    min_amount = request.args.get("min_amount", type=float)
    max_amount = request.args.get("max_amount", type=float)
    if min_amount is not None:
        query = query.filter(FinancialRecord.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(FinancialRecord.amount <= max_amount)

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    records = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": records.total,
        "pages": records.pages,
        "current_page": records.page,
        "records": [{
            "id": r.id,
            "amount": r.amount,
            "type": r.type,
            "category_id": r.category_id,
            "date": r.date,
            "notes": r.notes,
            "user_id": r.user_id
        } for r in records.items]
    }), 200


def get_record(record_id):
    record = FinancialRecord.query.filter_by(id=record_id, is_deleted=False).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({
        "id": record.id,
        "amount": record.amount,
        "type": record.type,
        "category_id": record.category_id,
        "date": record.date,
        "notes": record.notes,
        "user_id": record.user_id
    }), 200


def create_record():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        current_user_id = int(get_jwt_identity())
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid token identity"}), 401

    if not data.get("amount") or not data.get("type") or not data.get("category_id"):
        return jsonify({"error": "Amount, type and category are required"}), 400

    if data["type"] not in ["income", "expense"]:
        return jsonify({"error": "Type must be income or expense"}), 400

    if data["amount"] <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"error": "Invalid category_id"}), 400

    record = FinancialRecord(
        amount=data["amount"],
        type=data["type"],
        category_id=data["category_id"],
        user_id=current_user_id,
        notes=data.get("notes", ""),
        date=datetime.strptime(data["date"], "%Y-%m-%d") if data.get("date") else datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(record)

    # Log the action
    log = AuditLog(user_id=current_user_id, action=f"Created record of {data['type']} {data['amount']}")
    db.session.add(log)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Invalid record data"}), 400

    return jsonify({"message": "Record created successfully", "record_id": record.id}), 201


def update_record(record_id):
    record = FinancialRecord.query.filter_by(id=record_id, is_deleted=False).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404

    data = request.get_json()
    current_user_id = int(get_jwt_identity())

    if "amount" in data:
        if data["amount"] <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
        record.amount = data["amount"]
    if "type" in data:
        if data["type"] not in ["income", "expense"]:
            return jsonify({"error": "Type must be income or expense"}), 400
        record.type = data["type"]
    if "category_id" in data:
        record.category_id = data["category_id"]
    if "notes" in data:
        record.notes = data["notes"]
    if "date" in data:
        record.date = datetime.strptime(data["date"], "%Y-%m-%d")

    log = AuditLog(user_id=current_user_id, action=f"Updated record {record_id}")
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Record updated successfully"}), 200


def delete_record(record_id):
    record = FinancialRecord.query.filter_by(id=record_id, is_deleted=False).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404

    current_user_id = int(get_jwt_identity())

    # Soft delete
    record.is_deleted = True

    log = AuditLog(user_id=current_user_id, action=f"Deleted record {record_id}")
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Record deleted successfully"}), 200