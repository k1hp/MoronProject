from typing import Optional
from flask import request
from flasgger import swag_from
from flask_restx import Resource, Namespace, fields

from app.models.response_models import CommentResponseSchema
from database.flask_managers import DatabaseAdder, DatabaseSelector, DatabaseUpdater
from app.others.constants import TOKEN_LIFETIME
from app.others.helpers import Password, AccessToken, Token
from app.others.exceptions import ReIntegrityError, LackToken
from database.creation import db, Token, Profile
from app.others.middlewares import TokenService
from app.others.decorators import convert_error
from app.others.responses import CommentResponse, CustomResponse
from app.models.response_models import ProfileResponseSchema

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
        TokenService(request=request)
        u_id = (
            db.session.query(Token)
            .filter(Token.token == request.cookies["token"])
            .first()
            .user_id
        )
        profile = db.session.query(Profile).filter(Profile.user_id == u_id).first()
        return CustomResponse(model=ProfileResponseSchema(), data=profile).response

    @api.expect(profile_model)
    @convert_error
    def put(self):
        TokenService(request=request)
        return CommentResponse().success_response(
            comment="Данные были успешно обновлены."
        )
