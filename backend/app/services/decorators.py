import functools
from typing import Callable

from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask import Response

from backend.app.others.exceptions import (
    ReIntegrityError,
    LackToken,
    PasswordError,
    CookieTokenError,
    CookieTokenExistsError,
    EmailError,
    EmailIntegrityError,
    NicknameIntegrityError,
)
from backend.app.others.responses import CommentResponse


def clear_duplicates(function) -> Callable:
    """
    Убирает дубликаты словарей в списке или объектов в списке
    :param function:
    :return:
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs) -> list:
        result = function(*args, **kwargs)
        if isinstance(result[0], dict):
            return [dict(t) for t in set(tuple(dct.items()) for dct in result)]
        else:
            print(len(result), len(list(set(result))))
            return list(set(result))

    return wrapper


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
        except EmailIntegrityError as e:
            return response_object.failure_response(comment=e.__str__())

        except NicknameIntegrityError as e:
            return response_object.failure_response(comment=e.__str__())

        except PasswordError as e:
            return response_object.failure_response(comment=e.__str__())

        except EmailError as e:
            return response_object.failure_response(comment=e.__str__())

        except CookieTokenExistsError as e:
            return response_object.access_denied(comment=e.__str__())

        except CookieTokenError as e:
            print(e)
            return response_object.unauthorized(comment=e.__str__())

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
        # except ReIntegrityError as e:
        #     return response_object.failure_response(comment=e.__str__())

    return wrapper
