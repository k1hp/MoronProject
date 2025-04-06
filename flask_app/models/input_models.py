import marshmallow as ma


# Схема Marshmallow
class UserSchema(ma.Schema):
    login = ma.fields.Str(required=True)
    email = ma.fields.Email(required=True)
    password = ma.fields.Str(required=True)


class LoginEmailSchema(ma.Schema):
    login = ma.fields.Email(required=True)
    password = ma.fields.Str(required=True)


class LoginUsernameSchema(ma.Schema):
    login = ma.fields.Str(required=True)
    password = ma.fields.Str(required=True)


class ResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True)
    comment = ma.fields.Str(required=True)


class AuthorizationSchema(ma.Schema):
    login = ma.fields.Str(required=False)
    email = ma.fields.Email(required=False)
    password = ma.fields.Str(required=True)


response_schema = ResponseSchema()

bad_response_data = {"status": "BAD", "comment": "Data is not valid"}
success_response_data = {"status": "OK", "comment": "All the true"}

# Преобразуем словарь в JSON
bad_response = response_schema.dump(bad_response_data)
success_response = response_schema.dump(success_response_data)
