from app.extensions import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    records = db.relationship("FinancialRecord", backref="category_ref", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"