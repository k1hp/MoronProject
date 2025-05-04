import marshmallow as ma
from marshmallow.validate import Length


# Схема Marshmallow
class UserSchema(ma.Schema):
    # nickname = ma.fields.Str(
    #     required=True, validate=ma.validate.Length(min=1, max=20), example="sem4ik"
    # )
    # email = ma.fields.Email(
    #     required=True,
    #     validate=ma.validate.Length(min=3, max=100),
    #     example="sem@yandex.ru",
    # )
    # password = ma.fields.Str(
    #     required=True, validate=ma.validate.Length(min=8, max=100), example="1234"
    # )
    nickname = ma.fields.Str(required=True, example="sem4ik")
    email = ma.fields.Email(
        required=True,
        example="sem@yandex.ru",
    )
    password = ma.fields.Str(required=True, example="1234")
    # nickname = ma.fields.Str(required=True)
    # email = ma.fields.Email(required=True)
    # password = ma.fields.Str(required=True)


# class LoginEmailSchema(ma.Schema):
#     email = ma.fields.Email(required=True)
#     password = ma.fields.Str(required=True)


# class LoginUsernameSchema(ma.Schema):
#     login = ma.fields.Str(required=True)
#     password = ma.fields.Str(required=True)


class AuthorizationSchema(ma.Schema):
    email = ma.fields.Email(required=True, example="sem@yandex.ru")
    password = ma.fields.Str(required=True, example="1234")


class ProfileUpdateSchema(ma.Schema):
    nickname: ma.fields.String(required=False)
    status: ma.fields.String(required=False)
    photo_link: ma.fields.Url(required=False)
