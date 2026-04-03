from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="viewer")  # viewer / analyst / admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    records = db.relationship("FinancialRecord", backref="owner", lazy=True)
    logs = db.relationship("AuditLog", backref="actor", lazy=True)

    def __repr__(self):
        return f"<User {self.email} - {self.role}>"