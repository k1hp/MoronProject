import code
from abc import ABC, abstractmethod
import marshmallow as ma
from flask import Response as FlResponse, make_response
from typing import Optional

from flask_app.models.response_models import CommentResponseSchema
from others.constants import Status, Comment, StatusCode


class Response(ABC):
    def __init__(self, model_class: ma.Schema):
        self._model = model_class()

    @abstractmethod
    def _generate_response(self):
        pass


class CommentResponse(Response):
    def __init__(
        self,
        model_class: ma.Schema = CommentResponseSchema,
        statuses=Status,
        codes=StatusCode,
        comments=Comment,
    ):
        super().__init__(model_class)
        self._status = statuses
        self._codes = codes
        self._comments = comments

    def _generate_response(self, status: str, comment: str, code: int) -> FlResponse:
        data = self._model.dump({"status": status, "comment": comment})
        response = make_response(data, code)
        return response

    def success_response(self, comment: Optional[str] = None) -> FlResponse:
        status = self._status.SUCCESS
        comment = self._comments.SUCCESS if comment is None else comment
        code = self._codes.SUCCESS
        return self._generate_response(status, comment, code)

    def failure_response(self, comment: Optional[str] = None) -> FlResponse:
        status = self._status.FAILURE
        comment = self._comments.FAILURE if comment is None else comment
        code = self._codes.FAILURE
        return self._generate_response(status, comment, code)

    def access_denied(self, comment: Optional[str] = None) -> FlResponse:
        status = self._status.ACCESS_DENIED
        comment = self._comments.ACCESS_DENIED if comment is None else comment
        code = self._codes.ACCESS_DENIED
        return self._generate_response(status, comment, code)

    def not_found(self, comment: Optional[str] = None) -> FlResponse:
        status = self._status.NOT_FOUND
        comment = self._comments.NOT_FOUND if comment is None else comment
        code = self._codes.NOT_FOUND
        return self._generate_response(status, comment, code)

    def unauthorized(self, comment: Optional[str] = None) -> FlResponse:
        status = self._status.UNAUTHORIZED
        comment = self._comments.UNAUTHORIZED if comment is None else comment
        code = self._codes.UNAUTHORIZED
        return self._generate_response(status, comment, code)


class CustomCommentResponse(Response):
    def __init__(
        self,
        status: str,
        comment: str,
        code: int,
        model_class: ma.Schema = CommentResponseSchema,
    ):
        super().__init__(model_class)
        self.__response = self._generate_response(status, comment, code)

    def _generate_response(self, status: str, comment: str, code: int) -> FlResponse:
        data = self._model.dump({"status": status, "comment": comment})
        response = make_response(data, code)
        return response

    @property
    def response(self):
        return self.__response


class CookieResponse(Response):
    def __init__(
        self,
        response: Optional[FlResponse] = None,
        model_class: Optional[ma.Schema] = None,
        data: Optional[dict] = None,
        code: Optional[int] = None,
    ):
        if all(el is None for el in (response, model_class, data, code)):
            self.__response = self._emergency_response()
        elif response is None:
            super().__init__(model_class)
            self.__data = data
            self.__code = code
            self.__response = self._generate_response()
        else:
            self.__response = response

    def _generate_response(self) -> FlResponse:
        data = self._model.dump(self.__data)
        response = make_response(data, code)
        return response

    @staticmethod
    def _emergency_response() -> FlResponse:
        print("Ответ с куками, но без данных")
        return make_response({"status": "emergency"}, 204)

    def set_cookie(
        self,
        key: str,
        value: str,
        httponly: bool = False,
        age_days: Optional[int] = None,
    ) -> None:
        if age_days:
            age = 60 * 60 * 24 * age_days
        else:
            age = None
        self.__response.set_cookie(
            key=key,
            value=value,
            httponly=httponly,
            secure=True,
            samesite="Lax",
            max_age=age,
        )

    @property
    def response(self):
        return self.__response


# отдельный класс для генерации с куками, мы сможем выбирать куки сами
