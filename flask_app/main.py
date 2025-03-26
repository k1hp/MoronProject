from flask import Flask, request
from flask_restx import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, ValidationError

from database.creation import db
from settings import DB_CONNECTION
from flask_app.apis.test_bp import api as ns1

app = Flask(__name__)
api = Api(app)
api.add_namespace(ns1, path="/burger")

app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION
# initialize the app with the extension
db.init_app(app)

# with app.app_context():
#     db.create_all()



# Определяем модель для Swagger
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# Пример модели
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

# Схема Marshmallow
class UserSchema(Schema):
    username = ma_fields.Str(required=True)
    email = ma_fields.Email(required=True)

class ResponseSchema(Schema):
    status = ma_fields.Str(required=True)
    comment = ma_fields.Str(required=True)

user_schema = UserSchema()
response_schema = ResponseSchema()

bad_response_data = {"status": "BAD", "comment": "all bad"}
success_response_data = {"status": "OK", "comment": "nice work"}

# Преобразуем словарь в JSON
bad_response = response_schema.dump(bad_response_data)
success_response = response_schema.dump(success_response_data)

@api.route('/user', methods=["POST"])
class UserResource(Resource):
    @api.expect(user_model)  # Указываем, что ожидаем модель User
    def post(self):
        # Получаем JSON-данные
        json_data = request.json

        # Валидация и десериализация данных
        try:
            user_data = user_schema.load(json_data)  # Валидация данных
        except ValidationError as err:
            return bad_response, 400  # Возвращаем ошибки валидации

        return success_response, 201  # Возвращаем сериализованные данные пользователя


class Authorization(Resource):
    def post(self):
        json_data = request.json
        try:
            user_data = user_schema.load(json_data)  # Валидация данных
        except ValidationError as err:
            return bad_response, 400  # Возвращаем ошибки валидации

        return success_response, 201



class Tester:
    def print_ok(self):
        print("OK")
    def print_bad(self):
        print("NO")

if __name__ == '__main__':
    app.run(debug=True)
