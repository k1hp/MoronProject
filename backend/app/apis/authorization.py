from flask import request
from flask_restx import Resource, Namespace, fields

from backend.app.models.input_models import UserSchema, AuthorizationSchema
from backend.app.models.response_models import CommentResponseSchema
from backend.database.flask_managers import (
    DatabaseAdder,
)
from backend.app.others.constants import TOKEN_LIFETIME
from backend.app.services.helpers import Password
from backend.app.services.middlewares import (
    check_token_presence,
    check_cookies,
    AuthorizationService,
)
from backend.app.others.responses import CommentResponse, CookieResponse
from backend.app.services.decorators import convert_error

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
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "SUCCESS"
                        comment: "Пользователь успешно создан"
            '403':
              description: Пользователь не был создан
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "UNAUTHORIZED"
                        comment: "User is unauthorized"
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
            '201':
              description: Успешное создание пользователя
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "SUCCESS"
                        comment: "Пользователь успешно создан"
            '403':
              description: Пользователь не был создан
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "UNAUTHORIZED"
                        comment: "User is unauthorized"
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
            key="token", value=token.hash, httponly=True, age_days=TOKEN_LIFETIME
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
            '201':
              description: Успешное создание пользователя
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "SUCCESS"
                        comment: "Пользователь успешно создан"
            '403':
              description: Пользователь не был создан
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "UNAUTHORIZED"
                        comment: "User is unauthorized"
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
        cookie_response.set_cookie(key="token", value=token.hash, httponly=True)

        return cookie_response.response


@api.route("/token/logout", methods=["DELETE"])
class Logout(Resource):
    @convert_error
    def delete(self):
        """
        ---
          summary: Выход из аккаунта

          responses:
            '201':
              description: Успешное создание пользователя
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "SUCCESS"
                        comment: "Пользователь успешно создан"
            '403':
              description: Пользователь не был создан
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "UNAUTHORIZED"
                        comment: "User is unauthorized"
          tags:
            - Authorization
        """
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
