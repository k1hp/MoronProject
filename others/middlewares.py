from marshmallow import ValidationError
from typing import Optional

from database.managers import DatabaseSelector
from others.helpers import Password


def check_access_token(): ...


def check_login_data(json_data: dict) -> Optional[int]:
    selector = DatabaseSelector()
    new_data = json_data.copy()
    new_data.pop("password")
    new_data["password_hash"] = Password(json_data["password"]).hash
    return selector.select_user(**new_data)


def validate_data(schema, data) -> bool:  # pydentic и перенести всё в класс service
    try:
        schema.load(data)
    except ValidationError as err:
        return False
    return True


class ValidationService: ...
