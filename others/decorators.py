import functools

from sqlalchemy.exc import IntegrityError

from others.exceptions import ReIntegrityError


def integrity_check(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except IntegrityError as e:
            raise ReIntegrityError("Ошибка вставки данных. Скорее всего такая запись существует.")

    return wrapper