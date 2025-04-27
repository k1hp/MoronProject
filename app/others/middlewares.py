import marshmallow as ma
from typing import Optional
from flask import Request

from database.creation import db, User
from database.flask_managers import DatabaseSelector, TokenManager
from app.others.helpers import Password, AccessToken
from app.models.input_models import LoginEmailSchema
from app.others.exceptions import LackToken, CookieTokenError, LoginError, PasswordError
from database.flask_managers import get_token


class ServiceBase:
    # self._response_object = CommentResponse()
    # self._bad_response = self._response_object.failure_response()
    @staticmethod
    def _check_model(model_class: ma.Schema, data: dict):
        model = model_class()
        # model.validate(data)  не проверяет лишние параметры
        model.load(data)


class ValidationService(ServiceBase):
    def __init__(self, model_class: ma.Schema, data: dict):
        self._check_model(model_class, data)


class AuthorizationService(ServiceBase):
    def __init__(self, model_class: ma.Schema, request: Request):
        self._check_model(model_class, request.json)
        self.__selector = DatabaseSelector()
        self.__data = self._generate_login_data(request.json)
        self.__user = self._get_user()

    @staticmethod
    def _generate_login_data(data: dict) -> dict:
        result_data = {"password": data["password"]}
        try:
            LoginEmailSchema().load(data)
        except ma.ValidationError:
            return data
        result_data["email"] = data["login"]
        return result_data

    def _get_user(self) -> dict:
        if (
            "email" in self.__data
            and db.session.query(User).filter_by(email=self.__data["email"]).first()
            is None
        ):
            raise LoginError()
        elif (
            "login" in self.__data
            and db.session.query(User).filter_by(login=self.__data["login"]).first()
            is None
        ):
            raise LoginError()
        new_data = self.__data.copy()
        new_data.pop("password")
        new_data["password_hash"] = Password(self.__data["password"]).hash

        result = self.__selector.select_user(**new_data)
        if result is None:
            raise PasswordError()
        return result

    def get_token(self):
        user_id = self.__user.id
        result = self.__selector.select_token(user_id)
        if result is not None:  # возвращается токен если он уже есть в бд
            return result.token
        token = AccessToken()
        TokenManager(token).add_token(user_id)
        return token


class TokenService(ServiceBase):  # проверяет наличие токена и его валидность в бд
    def __init__(self, request: Request):
        self.__request = request
        self.__cookies = request.cookies
        self.__token = self.__exist_cookies_token()
        self.__is_active()

    def __exist_cookies_token(self) -> str:
        token = self.__cookies.get("token", None)
        if token is None:
            raise CookieTokenError()
        return token

    def __is_active(self) -> None:
        get_token(token=self.__token)

    # можно докинуть проверку на то что он не должен быть
    # в куках для повторной авторизации


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
        raise CookieTokenError("Токен уже есть в куках")
    return True
