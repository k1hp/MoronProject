from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

from backend.database.creation import db, User, Token, Profile
from typing import Optional

from backend.app.others.constants import TOKEN_LIFETIME
from backend.app.services.decorators import integrity_check
from backend.app.others.exceptions import (
    ParameterError,
    ReIntegrityError,
    LackToken,
    NicknameIntegrityError,
    EmailIntegrityError,
)
from backend.app.services.helpers import TokenBase as TokenType


class DatabaseManager:
    # def create_all(self): ...
    #
    # def drop_all(self): ...
    #
    # def drop_table(self, table: Base) -> None: ...
    @staticmethod
    def _add_data(object):
        db.session.add(object)
        db.session.commit()

    @staticmethod
    def _delete_data():
        pass


class TokenManager(DatabaseManager):
    def __init__(self, token: TokenType):
        self.__token = token.hash

    def add_token(self, user_id: int):
        user = Token(token=self.__token, user_id=user_id)
        self._add_data(user)

    def update_token(
        self, user_id: Optional[int] = None, old_token: Optional[str] = None
    ):
        if user_id is None and old_token is not None:
            token = db.session.query(Token).filter(Token.token == old_token).first()
        elif old_token is None and user_id is not None:
            token = db.session.query(Token).filter(Token.id == user_id).first()
        if token is None:
            raise ReIntegrityError("Такого пользователя не существует")
        token.token = self.__token
        db.session.commit()


class DatabaseAdder:
    def add_all(self): ...

    # @integrity_check
    def add_user(self, nickname: str, email: str, password: str) -> None:
        try:
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise EmailIntegrityError()

        user_id = db.session.query(User).filter(User.email == email).first().id

        try:
            profile = Profile(
                user_id=user_id, nickname=nickname, status=None, photo_link=None
            )
            db.session.add(profile)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise NicknameIntegrityError()

    @integrity_check
    def add_token(
        self,
        user_id: int,
        token: str,
    ):
        note = Token(
            user_id=user_id,
            token=token,
        )
        db.session.add(note)
        db.session.commit()

    def add_processors(self, data) -> None: ...


class DatabaseSelector:
    def select_user(
        self,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
    ) -> Optional[User]:

        return (
            db.session.query(User)
            .filter(and_(User.email == email, User.password == password_hash))
            .first()
        )

    def select_token(
        self, user_id: Optional[int] = None, token: Optional[str] = None
    ) -> Optional[Token]:
        if token is None and user_id is not None:
            return db.session.query(Token).filter(Token.user_id == user_id).first()
        elif user_id is None and token is not None:
            print(token)
            return db.session.query(Token).filter(Token.token == token).first()
        else:
            raise ParameterError


class DatabaseUpdater(DatabaseSelector):
    def update_token(self, user_id: int, new_token: str) -> None:
        data = self.select_token(user_id=user_id)
        data.token = new_token
        data.created_at = datetime.now()
        data.expired_at = data.created_at + timedelta(days=TOKEN_LIFETIME)
        db.session.commit()


def update_profile(profile: Profile, data: dict) -> None:
    for key, value in data.items():
        setattr(profile, key, value)
    db.session.add(profile)
    db.session.commit()


def get_token(
    user_id: Optional[int] = None, token: Optional[str] = None
) -> Optional[Token]:
    result = None
    if token is None and user_id is not None:
        result = db.session.query(Token).filter(Token.user_id == user_id).first()
    elif token is not None and user_id is None:
        result = db.session.query(Token).filter(Token.token == token).first()
    return check_active_token(token=result)


def check_active_token(token: Optional[Token]) -> Optional[Token]:
    if token is None:
        raise LackToken()

    if token.expired_at < datetime.now():
        db.session.delete(token)
        db.session.commit()
        raise LackToken()
    return token


if __name__ == "__main__":
    ...
