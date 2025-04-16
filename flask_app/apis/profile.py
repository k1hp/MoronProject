from typing import Optional

from flasgger import swag_from
from flask import request, make_response, Response, Request
from flask_restx import Resource, Namespace, fields

from flask_app.models.input_models import UserSchema, bad_response, success_response
from flask_app.models.response_models import CommentResponseSchema
from database.managers import DatabaseAdder, DatabaseSelector, DatabaseUpdater
from others.constants import TOKEN_LIFETIME
from others.helpers import Password, AccessToken, Token
from others.middlewares import (
    verify_token,
    validate_data,
    check_login_data,
    check_token_presence,
    check_cookies,
)
from others.exceptions import ReIntegrityError, LackToken
from others.responses import CommentResponse, Response as MyResponse

api = Namespace("profile", description="Information about profile")


@api.route("/profile")
class ProfileResource(Resource):
    def get(self):
        pass
