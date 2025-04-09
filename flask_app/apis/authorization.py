from typing import Optional

from flasgger import swag_from
from flask import request, make_response, Response, Request
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError

from flask_app.models.input_models import UserSchema, AuthorizationSchema
from database.managers import (
    DatabaseAdder,
    DatabaseSelector,
    DatabaseUpdater,
    TokenManager,
)
from others.constants import TOKEN_LIFETIME
from others.helpers import Password, AccessToken, Token
from others.middlewares import (
    verify_token,
    validate_data,
    check_login_data,
    check_token_presence,
    check_cookies,
    AuthorizationService,
)
from others.exceptions import ReIntegrityError, LackToken
from others.responses import CommentResponse, CookieResponse, Response as MyResponse
from others.decorators import convert_error
from others.settings import YAMLS_DIR

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


@api.route("/registration", methods=["POST"])
class Registration(Resource):
    @swag_from(YAMLS_DIR / "registration.yaml")
    @convert_error
    def post(self):
        """Example endpoint returning a list of colors by palette
        In this example the specification is taken from specs_dict
        """
        response = CommentResponse()
        db_adder = DatabaseAdder()
        json_data = request.json
        user_schema = UserSchema()
        if not validate_data(user_schema, json_data):
            print(json_data)
            return response.failure_response()

        password = Password(json_data["password"])
        db_adder.add_user(json_data["login"], json_data["email"], password.hash)

        return response.success_response()


@api.route("/token/auth", methods=["POST"])
class LoginToken(Resource):
    @api.expect(login_model)
    @convert_error
    def post(self):
        check_cookies(request)
        token = AuthorizationService(
            model_class=AuthorizationSchema, request=request
        ).get_token()
        success = CommentResponse().success_response("Вы были успешно авторизованы")
        cookie_response = CookieResponse(response=success)
        # cookie_response = CookieResponse()  # в emergency режиме (без данных)
        cookie_response.set_cookie(
            key="token", value=token.hash, httponly=True, age_days=TOKEN_LIFETIME
        )

        return cookie_response.response


@api.route("/token/auth/temporary", methods=["POST"])
class LoginTempToken(Resource):
    @api.expect(login_model)
    @convert_error
    def post(self):
        check_cookies(request)
        token = AuthorizationService(
            model_class=AuthorizationSchema, request=request
        ).get_token()
        success = CommentResponse().success_response("Вы были успешно авторизованы")
        cookie_response = CookieResponse(response=success)
        # cookie_response = CookieResponse()  # в emergency режиме (без данных)
        cookie_response.set_cookie(key="token", value=token.hash, httponly=True)

        return cookie_response.response


@api.route("/token/logout", methods=["DELETE"])
class Logout(Resource):
    @convert_error
    def delete(self):
        response = CommentResponse()
        if not check_token_presence(request=request):
            return response.access_denied(comment="You have not token")
        response = response.success_response(comment="Token has been deleted!")
        response.set_cookie(
            key="token", value="", httponly=True, secure=True, samesite="lax", max_age=0
        )
        return response


# @api.route("/token/refresh", methods=["PUT"])
# class TokenRefresher(Resource):
#     @convert_error
#     def put(self):
#         response = CommentResponse()
#         if not check_token_presence(request=request):
#             return response.access_denied(comment="You have not token")
#         cookies = dict(request.cookies)
#         token = cookies["token"]
#         try:
#             verify_token(token)
#         except LackToken:
#             return response.failure_response(comment="This token does not exists")
#         selector = DatabaseSelector()
#         updater = DatabaseUpdater()
#         user_id = selector.select_token(token=token).user_id
#         updater.update_token(
#             user_id, new_token=AccessToken().hash
#         )  # нужно подумать как лучше
#         # то есть мы обновим и потом оно вернет что токен есть в бд
#         response = set_response(
#             ({"status": "success", "comment": "token refreshed"}, 200),
#             user_id=user_id,
#             set_age=True,
#         )
#         return response
