from marshmallow import Schema, fields as ma_fields, ValidationError



# Определяем модель для Swagger


# Пример модели
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


# Схема Marshmallow
class UserSchema(Schema):
    login = ma_fields.Str(required=True)
    email = ma_fields.Email(required=True)
    password = ma_fields.Str(required=True)


class ResponseSchema(Schema):
    status = ma_fields.Str(required=True)
    comment = ma_fields.Str(required=True)


response_schema = ResponseSchema()

bad_response_data = {"status": "BAD", "comment": "Data is not valid"}
success_response_data = {"status": "OK", "comment": "All the true"}

# Преобразуем словарь в JSON
bad_response = response_schema.dump(bad_response_data)
success_response = response_schema.dump(success_response_data)
