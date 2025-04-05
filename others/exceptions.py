from sqlalchemy.exc import IntegrityError


class ParameterError(Exception):
    def __str__(self):
        return "Параметр передан неверно, или вовсе не был передан"


class ReIntegrityError(IntegrityError):
    def __str__(self):
        return "Ошибка вставки данных. Скорее всего такая запись существует."


class LackToken(Exception):
    def __str__(self):
        return "В бд нету такого токена"


class LoginError(Exception):
    def __str__(self):
        return "Неверный логин"


class PasswordError(Exception):
    def __str__(self):
        return "Неверный пароль"


class CookieTokenError(Exception):
    def __str__(self):
        return "В куках отсутствует токен или что-то еще связанное с ним"
