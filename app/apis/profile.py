from typing import Optional
from flask import request
from flasgger import swag_from
from flask_restx import Resource, Namespace, fields

from app.models.response_models import CommentResponseSchema
from database.flask_managers import DatabaseAdder, DatabaseSelector, DatabaseUpdater
from app.others.constants import TOKEN_LIFETIME
from app.others.helpers import Password, AccessToken, Token
from app.others.exceptions import ReIntegrityError, LackToken
from app.others.middlewares import TokenService
from app.others.decorators import convert_error
from app.others.decorators import CommentResponse

api = Namespace("profile", description="Information about profile")


@api.route("/profile")
class ProfileResource(Resource):
    @convert_error
    def get(self):
        TokenService(request=request)
        return CommentResponse().success_response()
