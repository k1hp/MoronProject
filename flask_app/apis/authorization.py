from typing import Optional

from flask import request, make_response, Response, Request
from flask_restx import Resource, Namespace, fields

from flask_app.models.input_models import UserSchema, bad_response, success_response
from database.managers import DatabaseAdder, DatabaseSelector, DatabaseUpdater
from others.helpers import Password, AccessToken, Token
from others.middlewares import (
    verify_token,
    validate_data,
    check_login_data,
    generate_correct_data,
    check_token_presence,
)
from others.exceptions import ReIntegrityError

api = Namespace("authorization", description="Authorization to you nice")

user_model = api.model(
    "User",
    {
        "login": fields.String(required=True, description="Username of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)

login_model = api.model(
    "Login/Username",
    {
        "login": fields.String(required=True, description="Login of the user"),
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


@api.route("/token/auth", methods=["POST"])
class LoginToken(Resource):
    @api.expect(login_model)
    def post(self):
        result = full_check_post(request)
        if result["code"] == 400:
            return result
        response = set_response(
            (result, result["code"]), user_id=result["user_id"], set_age=True
        )
        print(response)
        return response


@api.route("/token/auth/temporary", methods=["POST"])
class LoginTempToken(Resource):
    @api.expect(login_model)
    def post(self):
        result = full_check_post(request)
        if result["code"] == 400:
            return result
        response = set_response(
            (result, result["code"]), user_id=result["user_id"], set_age=False
        )
        print(response)
        return response


@api.route("/token/refresh", methods=["PUT"])
class TokenRefresher(Resource):
    def put(self):
        if not check_token_presence(request=request):
            return {"status": "error", "comment": "you have not token"}, 403
        cookies = dict(request.cookies)
        token = cookies["token"]
        if not verify_token(token):
            return {"status": "error", "comment": "your token does not exists"}, 400
        selector = DatabaseSelector()
        updater = DatabaseUpdater()
        user_id = selector.select_token(token=token).user_id
        updater.update_token(user_id=user_id, new_token=AccessToken().hash)
        # то есть мы обновим и потом оно вернет что токен есть в бд
        response = set_response(
            ({"status": "success", "comment": "token refreshed"}, 200),
            user_id=user_id,
            set_age=True,
        )
        return response


@api.route("/token/logout", methods=["DELETE"])
class Logout(Resource):
    def delete(self):
        if not check_token_presence(request=request):
            return {"status": "error", "comment": "you have not token"}, 400
        response = make_response(
            {"status": "success", "comment": "token deleted!"}, 200
        )
        response.set_cookie(
            key="token", value="", httponly=True, secure=True, samesite="lax", max_age=0
        )
        return response


def set_response(
    result: tuple, user_id: int, set_age: Optional[bool] = None
) -> Response:
    if set_age is True:
        age = 60 * 60 * 24 * 20
    else:
        age = None

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


def full_check_post(request: Request) -> dict:
    json_data = generate_correct_data(request.json)
    # email_schema = LoginEmailSchema()
    # if not validate_data(schema, json_data):
    #     return bad_response, 400
    user = check_login_data(json_data)
    if user is None:
        # нет такого пользователя либо пароль неверный
        return {"response": "success", "code": 400}

    user_id = user.id
    return {"response": "success", "user_id": user_id, "code": 200}


def create_token(token: Token, user_id: int) -> str:
    selector = DatabaseSelector()
    result = selector.select_token(user_id)
    if result is not None:  # возвращается токен если он уже есть в бд
        return result.token
    result = token.hash
    print(user_id)
    adder = DatabaseAdder()
    adder.add_token(user_id=user_id, token=result)

    return result
