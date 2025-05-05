from flask import request
from flask_restx import Resource, Namespace, fields

from backend.app.models.request_models import UserSchema, AuthorizationSchema
from backend.database.flask_managers import (
    DatabaseAdder,
)
from backend.app.others.constants import TOKEN_LIFETIME
from backend.app.services.helpers import Password
from backend.app.services.middlewares import (
    check_cookies,
    AuthorizationService,
    TokenService,
)
from backend.app.others.responses import CommentResponse, CookieResponse
from backend.app.services.decorators import convert_error
from backend.app.documentation.output_models import (
    CreatedResponseSchema,
    UnauthorizedResponseSchema,
    FailureRegistrationResponseSchema,
    SuccessResponseSchema,
    FailureAuthorizationResponseSchema,
    ExistsTokenAuthorizationFailure,
)

api = Namespace("authorization", description="Authorization to you nice")

user_model = api.model(
    "User",
    {
        "nickname": fields.String(
            required=True, description="Displayed nickname of the user"
        ),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)

login_model = api.model(
    "Login/Username",
    {
        "email": fields.String(required=True, description="Login of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)


@api.route("/registration", methods=["POST"])
class Registration(Resource):
    @convert_error
    def post(self):
        """
        ---
          summary: Создание нового пользователя
          parameters:
          - in: body
            schema: UserSchema


          responses:
            '201':
              description: Успешное создание пользователя
              schema: CreatedResponseSchema
            '400':
              description: Пользователь не был создан (Nickname или Email уже существуют)
              schema: FailureRegistrationResponseSchema
          tags:
            - Authorization
        """
        db_adder = DatabaseAdder()
        json_data = request.json
        UserSchema().load(json_data)

        password = Password(json_data["password"])
        db_adder.add_user(json_data["nickname"], json_data["email"], password.hash)

        return CommentResponse().created_response(comment="Пользователь успешно создан")


@api.route("/token/auth", methods=["POST"])
class LoginToken(Resource):

    @convert_error
    def post(self):
        """
        ---
          summary: Вход в аккаунт
          parameters:
          - in: body
            schema: AuthorizationSchema


          responses:
            '200':
              description: Успешная авторизация
              schema: SuccessResponseSchema
            '400':
              description: Какие-то данные введены неверно (password, email)
              schema: FailureAuthorizationResponseSchema
            '403':
              description: "Пользователь уже авторизован"
              schema: ExistsTokenAuthorizationFailure

          tags:
            - Authorization
        """
        check_cookies(request)
        token = AuthorizationService(
            model=AuthorizationSchema(), request=request
        ).get_token()
        success = CommentResponse().success_response("Вы были успешно авторизованы")
        cookie_response = CookieResponse(response=success)
        # cookie_response = CookieResponse()  # в emergency режиме (без данных)
        cookie_response.set_cookie(
            key="token", value=token, httponly=True, age_days=TOKEN_LIFETIME
        )

        return cookie_response.response


@api.route("/token/auth/temporary", methods=["POST"])
class LoginTempToken(Resource):
    @convert_error
    def post(self):
        """
        ---
          summary: ВРЕМЕННЫЙ вход в аккаунт
          parameters:
          - in: body
            schema: AuthorizationSchema


          responses:
            '200':
              description: Успешная авторизация
              schema: SuccessResponseSchema
            '400':
              description: Какие-то данные введены неверно (password, email)
              schema: FailureAuthorizationResponseSchema
            '403':
              description: "Пользователь уже авторизован"
              schema: ExistsTokenAuthorizationFailure

          tags:
            - Authorization
        """
        check_cookies(request)
        token = AuthorizationService(
            model=AuthorizationSchema(), request=request
        ).get_token()
        success = CommentResponse().success_response("Вы были успешно авторизованы")
        cookie_response = CookieResponse(response=success)
        # cookie_response = CookieResponse()  # в emergency режиме (без данных)
        cookie_response.set_cookie(key="token", value=token, httponly=True)

        return cookie_response.response


@api.route("/token/logout", methods=["DELETE"])
class Logout(Resource):
    @convert_error
    def delete(self):
        """
        ---
          summary: Выход из аккаунта

          responses:
            '200':
              description: Успешный выход из аккаунта
              schema: SuccessResponseSchema
            '401':
              description: Пользователь не авторизован
              schema: UnauthorizedResponseSchema
          tags:
            - Authorization
        """
        TokenService(request=request)
        response = CommentResponse().success_response(comment="Token has been deleted!")
        response.set_cookie(
            key="token", value="", httponly=True, secure=True, samesite="lax", max_age=0
        )
        return response
