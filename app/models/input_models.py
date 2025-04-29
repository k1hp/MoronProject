import marshmallow as ma


# Схема Marshmallow
class UserSchema(ma.Schema):
    nickname = ma.fields.Str(required=True)
    email = ma.fields.Email(required=True)
    password = ma.fields.Str(required=True)


# class LoginEmailSchema(ma.Schema):
#     email = ma.fields.Email(required=True)
#     password = ma.fields.Str(required=True)


# class LoginUsernameSchema(ma.Schema):
#     login = ma.fields.Str(required=True)
#     password = ma.fields.Str(required=True)


class ResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True)
    comment = ma.fields.Str(required=True)


class AuthorizationSchema(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.Str(required=True)
