import functools
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask import Response

from others.exceptions import (
    ReIntegrityError,
    LackToken,
    PasswordError,
    LoginError,
    CookieTokenError,
)
from others.responses import CommentResponse


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
            return response_object.failure_response(comment=e.__str__())

        except LackToken as e:
            return response_object.failure_response(comment=e.__str__())
        # except IntegrityError as e:
        #     return response_object.failure_response("")

    return wrapper
