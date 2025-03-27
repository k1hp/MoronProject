from flask import request
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError

from flask_app.models.test_models import UserSchema, bad_response, success_response
from database.managers import DatabaseAdder
from helpers import Password

api = Namespace('authorization', description='Nice dick, not your dick')

user_model = api.model('User', {
    'login': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route("/registration", methods=["POST"])
class Registration(Resource):
    @api.expect(user_model)
    def post(self):
        db_adder = DatabaseAdder()
        json_data = request.json
        user_schema = UserSchema()
        try:
            user_data = user_schema.load(json_data)  # Валидация данных
        except ValidationError as err:
            print(err)
            return bad_response, 400  # Возвращаем ошибки валидации

        password = Password(json_data["password"])
        db_adder.add_user(json_data["login"], json_data["email"], password.hash)

        return success_response, 201


class TokenGetter(Resource):
    ...

class TokenRefresher(Resource):
    ...