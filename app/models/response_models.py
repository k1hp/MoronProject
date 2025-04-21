import marshmallow as ma


class CommentResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True)
    comment = ma.fields.Str(required=True)
