import functools
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask import Response

from app.others.exceptions import (
    ReIntegrityError,
    LackToken,
    PasswordError,
    LoginError,
    CookieTokenError,
)
from app.others.responses import CommentResponse, CookieResponse


def integrity_check(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except IntegrityError as e:
            raise ReIntegrityError(
                "Ошибка вставки данных. Скорее всего такая запись существует."
            )

    return wrapper


def convert_error(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs) -> Response:
        response_object = CommentResponse()
        try:
            return function(*args, **kwargs)
        except ValidationError:
            # какой-то лог
            return response_object.failure_response(
                comment="Данные не прошли проверку в модели marshmallow"
            )
        except PasswordError as e:
            return response_object.failure_response(comment=e.__str__())

        except LoginError as e:
            return response_object.failure_response(comment=e.__str__())

        except CookieTokenError as e:
            print(e)
            return response_object.access_denied(comment=e.__str__())

        except LackToken as e:
            response = response_object.failure_response(comment=e.__str__())
            # cookie_response = CookieResponse(response=response)
            # cookie_response.set_cookie(key="token", value="None", age_days=0)
            # return cookie_response.response  # сброс токена в куках
            response.set_cookie(
                key="token",
                value="",
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=0,
            )
            return response
        # except IntegrityError as e:
        #     return response_object.failure_response("")

    return wrapper
