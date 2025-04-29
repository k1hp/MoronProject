from typing import Optional
from flask import request
from flasgger import swag_from
from flask_restx import Resource, Namespace, fields

from app.models.response_models import CommentResponseSchema
from database.flask_managers import (
    DatabaseAdder,
    DatabaseSelector,
    DatabaseUpdater,
    update_profile,
)
from app.others.constants import TOKEN_LIFETIME
from app.others.exceptions import ReIntegrityError, LackToken
from database.creation import db, Token, Profile

from app.others.helpers import get_profile
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
        token = TokenService(request=request).token
        profile = get_profile(token)
        return CustomResponse(model=ProfileResponseSchema(), data=profile).response

    @api.expect(profile_model)
    @convert_error
    def put(self):
        token = TokenService(request=request).token
        update_profile(get_profile(token), request.json)
        return CommentResponse().success_response(
            comment="Данные были успешно обновлены."
        )
