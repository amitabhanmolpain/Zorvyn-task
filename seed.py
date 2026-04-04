from datetime import datetime

from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.category import Category
from app.models.financial_record import FinancialRecord


def seed():
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(
            name="Admin User",
            email="admin@example.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="admin",
            is_active=True
        )
        analyst = User(
            name="Analyst User",
            email="analyst@example.com",
            password=bcrypt.generate_password_hash("analyst123").decode("utf-8"),
            role="analyst",
            is_active=True
        )
        viewer = User(
            name="Viewer User",
            email="viewer@example.com",
            password=bcrypt.generate_password_hash("viewer123").decode("utf-8"),
            role="viewer",
            is_active=True
        )

        db.session.add_all([admin, analyst, viewer])

        categories = [
            Category(name="Salary"),
            Category(name="Food"),
            Category(name="Rent"),
            Category(name="Transport"),
            Category(name="Freelance"),
            Category(name="Utilities")
        ]
        db.session.add_all(categories)
        db.session.flush()

        category_map = {c.name: c.id for c in categories}

        records = [
            FinancialRecord(amount=50000, type="income", category_id=category_map["Salary"], user_id=admin.id, date=datetime(2024, 1, 5), notes="January salary"),
            FinancialRecord(amount=1200, type="expense", category_id=category_map["Food"], user_id=admin.id, date=datetime(2024, 1, 8), notes="Groceries"),
            FinancialRecord(amount=15000, type="expense", category_id=category_map["Rent"], user_id=analyst.id, date=datetime(2024, 1, 10), notes="Monthly rent"),
            FinancialRecord(amount=3000, type="income", category_id=category_map["Freelance"], user_id=analyst.id, date=datetime(2024, 1, 22), notes="Design project"),
            FinancialRecord(amount=900, type="expense", category_id=category_map["Transport"], user_id=viewer.id, date=datetime(2024, 2, 3), notes="Commute"),
            FinancialRecord(amount=2200, type="expense", category_id=category_map["Utilities"], user_id=viewer.id, date=datetime(2024, 2, 14), notes="Electricity and internet"),
            FinancialRecord(amount=52000, type="income", category_id=category_map["Salary"], user_id=admin.id, date=datetime(2024, 2, 28), notes="February salary")
        ]

        db.session.add_all(records)
        db.session.commit()

    print("Seed completed successfully.")
    print("Credentials:")
    print("admin@example.com / admin123")
    print("analyst@example.com / analyst123")
    print("viewer@example.com / viewer123")


if __name__ == "__main__":
    seed()