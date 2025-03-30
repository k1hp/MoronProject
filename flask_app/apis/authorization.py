from typing import Optional

from flask import request, make_response, Response
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
from others.helpers import Password, AccessToken, Token
from others.middlewares import validate_data, check_login_data

api = Namespace("authorization", description="Authorization to you nice")

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
class UsernameToken(Resource):
    @api.expect(username_login_model)
    def post(self):
        schema = LoginUsernameSchema()
        result = full_check_post(request, schema)
        if result[-1] == 400:
            return result
        response = set_response(result, set_age=True)
        print(response)
        return response


@api.route("/token/auth/temp_username", methods=["POST"])
class UsernameTempToken(Resource):
    @api.expect(username_login_model)
    def post(self):
        schema = LoginUsernameSchema()
        result = full_check_post(request, schema)
        if result[-1] == 400:
            return result
        response = set_response(result, set_age=False)
        print(response)
        return response


@api.route("/token/auth/email", methods=["POST"])
class EmailToken(Resource):
    @api.expect(email_login_model)
    def post(self):
        schema = LoginEmailSchema()
        result = full_check_post(request, schema)
        if result[-1] == 400:
            return result
        response = set_response(result, set_age=True)
        print(response)
        return response


@api.route("/token/auth/temp_email", methods=["POST"])
class EmailTempToken(Resource):
    @api.expect(email_login_model)
    def post(self):
        schema = LoginEmailSchema()
        result = full_check_post(request, schema)
        if result[-1] == 400:
            return result
        response = set_response(result, set_age=False)
        print(response)
        return response


def set_response(result: tuple, set_age: Optional[bool] = None) -> Response:
    if set_age is True:
        age = 60 * 60 * 24 * 20
    else:
        age = None

    user_id = result[0]["user_id"]
    print(*result)
    response = make_response(*result)
    print(response)
    response.set_cookie(
        key="token",
        value=create_token(token=AccessToken(), user_id=user_id),
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=age,
    )
    return response


def full_check_post(request, schema):
    json_data = request.json
    # email_schema = LoginEmailSchema()
    if not validate_data(schema, json_data):
        return bad_response, 400
    user = check_login_data(json_data)
    if user is None:
        # нет такого пользователя либо пароль неверный
        return bad_response, 400

    user_id = user.id
    return {"user_id": user_id}, 200


def create_token(token: Token, user_id: int) -> str:
    result = token.hash
    device = "parfenov"
    print(user_id)
    adder = DatabaseAdder()
    adder.add_token(user_id=user_id, token=result, device=device)
    return result


# def get_success_token():


# def get_bad_token():

#
#     # можно сериализировать сразу класс токена и тп


@api.route("/token/refresh", methods=["POST"])
class TokenRefresher(Resource): ...
