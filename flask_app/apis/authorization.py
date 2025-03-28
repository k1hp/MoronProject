from flask import request
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError

from flask_app.models.test_models import (
    UserSchema,
    bad_response,
    success_response,
    LoginEmailSchema,
    LoginUsernameSchema,
)
from database.managers import DatabaseAdder
from others.helpers import Password, AccessToken
from others.middlewares import validate_data, check_login_data

api = Namespace("authorization", description="Nice dick, not your dick")

user_model = api.model(
    "User",
    {
        "login": fields.String(required=True, description="Username of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)

username_login_model = api.model(
    "Login/Username",
    {
        "login": fields.String(required=True, description="Login of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)

email_login_model = api.model(
    "Login/Email",
    {
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)


@api.route(
    "/registration", methods=["POST"]
)  # нужно определенные значения возвращать при случаях существующего аккаунта и тп
class Registration(Resource):
    @api.expect(user_model)
    def post(self):
        db_adder = DatabaseAdder()
        json_data = request.json
        user_schema = UserSchema()
        if not validate_data(user_schema, json_data):
            return bad_response, 400

        password = Password(json_data["password"])
        db_adder.add_user(json_data["login"], json_data["email"], password.hash)

        return success_response, 201


@api.route("/token/auth/username", methods=["POST"])
class UsernameTokenGetter(Resource):
    @api.expect(username_login_model)
    def post(self):
        json_data = request.json
        username_schema = LoginUsernameSchema()
        if not validate_data(username_schema, json_data):
            return bad_response, 400
        user_id = check_login_data(json_data)
        if user_id is None:
            # нет такого пользователя либо пароль неверный
            return bad_response, 400

        return {"token": AccessToken().hash}, 200


@api.route("/token/auth/email", methods=["POST"])
class EmailTokenGetter(Resource):
    @api.expect(email_login_model)
    def post(self):
        json_data = request.json
        email_schema = LoginEmailSchema()
        if not validate_data(email_schema, json_data):
            return bad_response, 400
        user_id = check_login_data(json_data)
        if user_id is None:
            # нет такого пользователя либо пароль неверный
            return bad_response, 400

        return {"token": AccessToken().hash}, 200

    # можно сериализировать сразу класс токена и тп


@api.route("/token/refresh", methods=["POST"])
class TokenRefresher(Resource): ...
