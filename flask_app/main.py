from flask import Flask, request
from flask_restx import Api, Resource

from database.creation import db
from others.settings import DB_CONNECTION
from flask_app.apis.authorization import api as ns1, email_post, email_login_model
from database.managers import DatabaseAdder, DatabaseSelector
from others.helpers import AccessToken, RefreshToken, Password

app = Flask(__name__)
api = Api(app)
api.add_namespace(ns1, path="/api")

app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.drop_all()

with app.app_context():
    db.create_all()

with app.app_context():
    adder = DatabaseAdder()
    access_token = AccessToken().hash
    adder.add_user("nigger", "4@yandex.ru", Password("1234").hash)
    # adder.add_tokens(1, "d", access_token, RefreshToken().hash, revoked=True)
    # try:
    #     adder.add_tokens(1, "d", access_token, RefreshToken().hash, revoked=True)
    # except ValueError as e:
    #     print(e)

# with app.app_context():
#     selector = DatabaseSelector()
#     hash = Password("<PASSWORD>").hash
#     print(selector.select_user(login="nigger", password_hash=hash))

# Определяем модель для Swagger
# user_model = api.model('User', {
#     'username': fields.String(required=True, description='Username of the user'),
#     'email': fields.String(required=True, description='Email of the user')
# })


# Пример модели
# class User:
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
# # Схема Marshmallow
# class UserSchema(Schema):
#     username = ma_fields.Str(required=True)
#     email = ma_fields.Email(required=True)
#
# class ResponseSchema(Schema):
#     status = ma_fields.Str(required=True)
#     comment = ma_fields.Str(required=True)
#
# user_schema = UserSchema()
# response_schema = ResponseSchema()
#
# bad_response_data = {"status": "BAD", "comment": "all bad"}
# success_response_data = {"status": "OK", "comment": "nice work"}
#
# # Преобразуем словарь в JSON
# bad_response = response_schema.dump(bad_response_data)
# success_response = response_schema.dump(success_response_data)
#
# @api.route('/user', methods=["POST"])
# class UserResource(Resource):
#     @api.expect(user_model)  # Указываем, что ожидаем модель User
#     def post(self):
#         # Получаем JSON-данные
#         json_data = request.json
#
#         # Валидация и десериализация данных
#         try:
#             user_data = user_schema.load(json_data)  # Валидация данных
#         except ValidationError as err:
#             return bad_response, 400  # Возвращаем ошибки валидации
#
#         return success_response, 201  # Возвращаем сериализованные данные пользователя
#
#
# class Authorization(Resource):
#     def post(self):
#         json_data = request.json
#         try:
#             user_data = user_schema.load(json_data)  # Валидация данных
#         except ValidationError as err:
#             return bad_response, 400  # Возвращаем ошибки валидации
#
#         return success_response, 201
#
@api.route("/token/auth/email", methods=["POST"])
class EmailToken(Resource):
    @api.expect(email_login_model)
    def post(self):
        result = email_post(request)
        if result[-1] == 400:
            return result
        response = api.make_response({"another token": AccessToken().hash}, 201)
        response.set_cookie(
            key="token",
            value=AccessToken().hash,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 20,
        )
        return response


@api.route("/token/auth/tempemail", methods=["POST"])
class EmailTempToken(Resource):
    @api.expect(email_login_model)
    def post(self):
        result = email_post(request)
        if result[-1] == 400:
            return result
        response = api.make_response({"another token": AccessToken().hash}, 201)
        response.set_cookie(
            key="token",
            value=AccessToken().hash,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return response


if __name__ == "__main__":
    app.run(debug=True)
