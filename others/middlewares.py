import marshmallow as ma
from typing import Optional
from flask import Request

from database.managers import DatabaseSelector
from others.helpers import Password
from flask_app.models.input_models import LoginEmailSchema, LoginUsernameSchema
from others.exceptions import LackToken
from others.responses import CommentResponse


class ValidationBase:
        # self._response_object = CommentResponse()
        # self._bad_response = self._response_object.failure_response()
    @staticmethod
    def check_model(model_class: ma.Schema, data: dict):
        model = model_class()
        model.validate(data)


class ValidationService(ValidationBase):
    def __init__(self, model_class: ma.Schema, data: dict):
        self.check_model(model_class, data)

    def


def generate_correct_data(data: dict) -> dict:
    result_data = {"password": data["password"]}
    email_schema = LoginEmailSchema()
    try:
        email_schema.load(data)
    except ma.ValidationError:
        return data
    result_data["email"] = data["login"]
    return result_data

class TokenService(ValidationBase):
    def __init__(self):
        pass

def check_token_presence(request: Request) -> bool:
    cookies = dict(request.cookies)
    print("Куки:", cookies.keys())
    if "token" not in cookies.keys():
        return False
    return True


def check_login_data(json_data: dict) -> Optional[int]:
    selector = DatabaseSelector()
    new_data = json_data.copy()
    new_data.pop("password")
    new_data["password_hash"] = Password(json_data["password"]).hash
    return selector.select_user(**new_data)


def validate_data(schema, data) -> bool:  # pydentic и перенести всё в класс service
    try:
        schema.load(data)
    except ma.ValidationError as err:
        return False
    return True


def verify_token(token: str) -> None:
    print(token)
    selector = DatabaseSelector()
    # result = selector.select_token(token=token)
    # print(result)
    if selector.select_token(token=token) is None:
        raise LackToken()


def check_cookies(request: Request) -> bool:
    if "token" in dict(request.cookies):
        raise ValueError("Токен уже есть в куках")
    return True
