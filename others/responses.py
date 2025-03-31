from abc import ABC, abstractmethod
import marshmallow as ma
from flask import Response as FlResponse, make_response

from flask_app.models.response_models import CommentResponseSchema
from others.constants import Status, Comment, StatusCode


class Response(ABC):
    def __init__(self, model):
        self._model = model

    @abstractmethod
    def _generate_response(self):
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

    def _generate_response(self, status, comment, code) -> FlResponse:
        data = self._model.dump({"status": status, "comment": comment})
        response = make_response(data, code)
        return response

    def success_response(self) -> FlResponse:
        status = self._status.SUCCESS
        comment = self._comments.SUCCESS
        code = self._codes.SUCCESS
        return self._generate_response(status, comment, code)

    def failure_response(self) -> FlResponse:
        status = self._status.FAILURE
        comment = self._comments.FAILURE
        code = self._codes.FAILURE
        return self._generate_response(status, comment, code)


class CustomCommentResponse(Response):
    def __init__(
        self,
        status,
        code,
        comment,
        model: ma.Schema = CommentResponseSchema(),
    ):
        super().__init__(model)
        self.__response = self._generate_response(status, comment, code)

    def _generate_response(self, status, comment, code):
        data = self._model.dump({"status": status, "comment": comment})
        response = make_response(data, code)
        return response

    @property
    def response(self):
        return self.__response


# отдельный класс для генерации с куками, мы сможем вырать куки сами
