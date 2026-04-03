from app.extensions import ma
from app.models.category import Category
from marshmallow import fields, validate

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

    name = fields.String(required=True, validate=validate.Length(min=2, max=50))