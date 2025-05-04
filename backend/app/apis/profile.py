from flask import request
from flask_restx import Resource, Namespace, fields

from backend.database.flask_managers import (
    update_profile,
)
from backend.app.services.helpers import get_profile
from backend.app.services.middlewares import TokenService
from backend.app.services.decorators import convert_error
from backend.app.others.responses import CommentResponse, CustomResponse
from backend.app.models.response_models import (
    ProfileResponseSchema,
    CommentResponseSchema,
)
from backend.app.documentation.output_models import (
    UnauthorizedResponseSchema,
    SuccessResponseSchema,
)

api = Namespace("profile", description="Information about profile")

profile_model = api.model(
    "Profile",
    {
        "nickname": fields.String(),
        "status": fields.String(),
        "photo_link": fields.String(),
    },
)


@api.route("/profile")
class ProfileResource(Resource):

    @convert_error
    def get(self):
        """
        ---
          summary: Получение простой информации о пользователе
          responses:
            '200':
              description: Успешное получение информации
              schema: SuccessResponseSchema

            '401':
              description: Пользователь не авторизован, нужно перенаправить на авторизацию
              schema: UnauthorizedResponseSchema

          tags:
            - Profile
        """
        token = TokenService(request=request).token
        profile = get_profile(token)
        return CustomResponse(model=ProfileResponseSchema(), data=profile).response

    # @api.expect(profile_model)
    @convert_error
    def put(self):
        """
        ---
          summary: Обновление простой информации о пользователе
          parameters:
          - in: body
            name: body
            description: "Данные на обновление пользователя"
            schema:
              type: object
              properties:
                nickname:
                  type: string
                  description: "Отображаемое имя пользователя."
                  example: "ya macan"
                photo_link:
                  type: string
                  description: "Ссылка на аватарку пользователя."
                  example: "https://i1.sndcdn.com/artworks-b8vZs1TN28AFyDpi-JHQM6w-t1080x1080.png"
                status:
                  type: string
                  description: "Статус-текст пользователя."
                  example: "следите за мной на моём youtube account и vk.com/timati"


          responses:
            '200':
              description: Данные были успешно обновлены
              schema:
                type: object
                properties:
                  status:
                    type: string
                    description: "Статус ответа"
                    example: "SUCCESS"
                  comment:
                    type: string
                    description: "Коммент"
                    example: "Данные были успешно обновлены."
            '401':
              description: Пользователь не авторизован, нужно перенаправить на авторизацию
              schema: UnauthorizedResponseSchema

          tags:
            - Profile
        """
        print(request.cookies, request.json)
        token = TokenService(request=request).token
        update_profile(get_profile(token), request.json)
        return CommentResponse().success_response(
            comment="Данные были успешно обновлены."
        )
