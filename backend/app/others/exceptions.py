from sqlalchemy.exc import IntegrityError
from typing import Optional


class MyException(Exception):
    def __init__(self, message: Optional[str] = None):
        self._message = message


class ParameterError(MyException):
    def __str__(self):
        if self._message is None:
            return "Параметр передан неверно, или вовсе не был передан"
        return self._message


class ReIntegrityError(IntegrityError):
    def __str__(self):
        return "Ошибка вставки данных. Скорее всего такая запись существует."


class LackToken(MyException):
    def __str__(self):
        if self._message is None:
            return "В бд нету такого токена"
        return self._message


class NicknameIntegrityError(MyException):
    def __str__(self):
        if self._message is None:
            return "Пользователь с таким Nickname уже существует"
        return self._message


class EmailIntegrityError(MyException):
    def __str__(self):
        if self._message is None:
            return "Пользователь с таким Email уже существует"
        return self._message


class EmailError(MyException):
    def __str__(self):
        if self._message is None:
            return "Неверный email"
        return self._message


class PasswordError(MyException):
    def __str__(self):
        if self._message is None:
            return "Неверный пароль"
        return self._message


class CookieTokenExistsError(MyException):
    def __str__(self):
        if self._message is None:
            return "Токен уже есть в куках."
        return self._message


class CookieTokenError(MyException):
    def __str__(self):
        if self._message is None:
            return "В куках отсутствует токен или что-то еще связанное с ним"
        return self._message
