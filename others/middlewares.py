from marshmallow import ValidationError
from typing import Optional
from flask import Request

from database.managers import DatabaseSelector
from others.helpers import Password
from flask_app.models.input_models import LoginEmailSchema, LoginUsernameSchema


def generate_correct_data(data: dict) -> dict:
    result_data = {"password": data["password"]}
    email_schema = LoginEmailSchema()
    try:
        email_schema.load(data)
    except ValidationError:
        return data
    result_data["email"] = data["login"]
    return result_data


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
    except ValidationError as err:
        return False
    return True


def verify_token(token: str) -> bool:
    print(token)
    selector = DatabaseSelector()
    # result = selector.select_token(token=token)
    # print(result)
    if selector.select_token(token=token) is None:
        return False
    return True


class ValidationService: ...
