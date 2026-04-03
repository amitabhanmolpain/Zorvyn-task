from app.extensions import ma
from app.models.audit_log import AuditLog
from marshmallow import fields

class AuditLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuditLog
        load_instance = True

    timestamp = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)