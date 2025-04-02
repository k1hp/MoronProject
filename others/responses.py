from abc import ABC, abstractmethod
import marshmallow as ma
from flask import Response as FlResponse, make_response
from typing import Optional

from flask_app.models.response_models import CommentResponseSchema
from others.constants import Status, Comment, StatusCode


class Response(ABC):
    def __init__(self, model):
        self._model = model

    @abstractmethod
    def _generate_response(self, status: str, comment: str, code: int):
        pass


class CommentResponse(Response):
    def __init__(
        self,
        model: ma.Schema = CommentResponseSchema(),
        statuses=Status,
        codes=StatusCode,
        comments=Comment,
    ):
        super().__init__(model)
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
        model: ma.Schema = CommentResponseSchema(),
    ):
        super().__init__(model)
        self.__response = self._generate_response(status, comment, code)

    def _generate_response(self, status: str, comment: str, code: int) -> FlResponse:
        data = self._model.dump({"status": status, "comment": comment})
        response = make_response(data, code)
        return response

    @property
    def response(self):
        return self.__response


# отдельный класс для генерации с куками, мы сможем выбирать куки сами
