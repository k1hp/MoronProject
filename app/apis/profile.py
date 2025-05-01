from typing import Optional
from flask import request
from flask_restx import Resource, Namespace, fields

from database.flask_managers import (
    update_profile,
)
from app.others.helpers import get_profile
from app.others.middlewares import TokenService
from app.others.decorators import convert_error
from app.others.responses import CommentResponse, CustomResponse
from app.models.response_models import ProfileResponseSchema, CommentResponseSchema
from app.models.input_models import ProfileUpdateSchema

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
              content:
                application/json:
                  schema: ProfileResponseSchema
                  examples:
                    example:
                      summary: Пример успешного ответа
                      value:
                        status: "my status ahahahha"
                        photo_link: "https://i1.sndcdn.com/artworks-b8vZs1TN28AFyDpi-JHQM6w-t1080x1080.png"
                        nickname: "Egorch1k"
            '401':
              description: Пользователь не авторизован, нужно перенаправить на авторизацию
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "UNAUTHORIZED"
                        comment: "User is unauthorized"
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
            required: true
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
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "SUCCESS"
                        comment: "Данные были успешно обновлены"
            '401':
              description: Пользователь не авторизован, нужно перенаправить на авторизацию
              content:
                application/json:
                  schema: CommentResponseSchema
                  examples:
                    example:
                      value:
                        status: "UNAUTHORIZED"
                        comment: "User is unauthorized"
          tags:
            - Profile
        """
        token = TokenService(request=request).token
        update_profile(get_profile(token), request.json)
        return CommentResponse().success_response(
            comment="Данные были успешно обновлены."
        )
