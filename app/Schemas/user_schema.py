from app.extensions import ma
from app.models.user import User
from marshmallow import fields, validate

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password",)

    email = fields.Email(required=True)
    role = fields.String(validate=validate.OneOf(["viewer", "analyst", "admin"]))
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))