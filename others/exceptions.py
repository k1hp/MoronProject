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
