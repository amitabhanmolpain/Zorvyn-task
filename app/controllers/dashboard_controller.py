from flask import jsonify
from app.extensions import db
from app.models.financial_record import FinancialRecord
from sqlalchemy import func

def get_summary():
    # Total income
    total_income = db.session.query(
        func.sum(FinancialRecord.amount)
    ).filter_by(type="income", is_deleted=False).scalar() or 0

    # Total expenses
    total_expense = db.session.query(
        func.sum(FinancialRecord.amount)
    ).filter_by(type="expense", is_deleted=False).scalar() or 0

    # Net balance
    net_balance = total_income - total_expense

    # Category wise totals
    category_totals = db.session.query(
        FinancialRecord.category_id,
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter_by(is_deleted=False).group_by(
        FinancialRecord.category_id,
        FinancialRecord.type
    ).all()

    # Monthly trends
    monthly_trends = db.session.query(
        func.strftime("%Y-%m", FinancialRecord.date).label("month"),
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter_by(is_deleted=False).group_by("month", FinancialRecord.type).all()

    # Recent 5 records
    recent = FinancialRecord.query.filter_by(
        is_deleted=False
    ).order_by(FinancialRecord.created_at.desc()).limit(5).all()

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "category_totals": [
            {"category_id": c.category_id, "type": c.type, "total": c.total}
            for c in category_totals
        ],
        "monthly_trends": [
            {"month": m.month, "type": m.type, "total": m.total}
            for m in monthly_trends
        ],
        "recent_activity": [
            {"id": r.id, "amount": r.amount, "type": r.type, "date": r.date}
            for r in recent
        ]
    }), 200