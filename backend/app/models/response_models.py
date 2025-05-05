import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from backend.database.creation import Profile, Processor


class CommentResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True)
    comment = ma.fields.Str(required=True)


class ProfileResponseSchema(SQLAlchemyAutoSchema):  # попробовать связать с orm
    class Meta:
        model = Profile


class ProcessorResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Processor
        fields = ("name", "socket", "TDP", "price")
        # exclude = ("id",)
        # # exclude = ("T", "secret_attribute")


class ProcessorFullResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Processor
        exclude = ("id",)
        # fields = ("name", "socket", "core", "TDP", "price")
        # # exclude = ("T", "secret_attribute")
