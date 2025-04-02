from sqlalchemy import and_
from datetime import datetime, timedelta

from database.creation import db, Base, User, Token
from typing import Optional, List

from others.constants import TOKEN_LIFETIME
from others.decorators import integrity_check
from others.exceptions import ParameterError


class DatabaseManager:
    def create_all(self): ...

    def drop_all(self): ...

    def drop_table(self, table: Base) -> None: ...


class DatabaseAdder:
    def add_all(self): ...

    @integrity_check
    def add_user(self, login: str, email: str, password: str) -> None:
        user = User(login=login, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    @integrity_check
    def add_token(
        self,
        user_id: int,
        token: str,
        revoked: Optional[bool] = None,
    ):
        if revoked is None:
            revoked = 0
        note = Token(
            user_id=user_id,
            token=token,
            revoked=revoked,
        )
        db.session.add(note)
        db.session.commit()


class DatabaseSelector:
    def select_user(
        self,
        login: Optional[str] = None,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
    ) -> Optional[User]:
        result = None
        if login is None:
            print(email)
            result = (
                db.session.query(User)
                .filter(and_(User.email == email, User.password == password_hash))
                .first()
            )
        elif email is None:
            print(login)
            result = (
                db.session.query(User)
                .filter(and_(User.login == login, User.password == password_hash))
                .first()
            )
        return result

    def select_token(
        self, user_id: Optional[int] = None, token: Optional[str] = None
    ) -> Token:
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


if __name__ == "__main__":
    adder = DatabaseAdder()
    adder.add_user("nigger", "<EMAIL>", "<PASSWORD>")
    # adder.add_tokens(1, "d", "ds", "fdsf")
