import functools

from sqlalchemy.exc import IntegrityError

def integrity_check(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except IntegrityError:
            raise ValueError("DatabaseIntegrityError")

    return wrapper