from app.extensions import ma
from app.models.financial_record import FinancialRecord
from marshmallow import fields, validate

class RecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FinancialRecord
        load_instance = True
        exclude = ("is_deleted",)

    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    type = fields.String(required=True, validate=validate.OneOf(["income", "expense"]))
    category_id = fields.Integer(required=True)
    date = fields.DateTime(required=False)
    notes = fields.String(validate=validate.Length(max=300))