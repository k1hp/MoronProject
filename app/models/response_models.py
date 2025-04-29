import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from database.creation import Profile


class CommentResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True)
    comment = ma.fields.Str(required=True)


class ProfileResponseSchema(SQLAlchemyAutoSchema):  # попробовать связать с orm
    class Meta:
        model = Profile
