from sqlalchemy import and_

from database.creation import db, Base, User, Token
from typing import Optional, List
from others.decorators import integrity_check


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
        device: str,
        token: str,
        revoked: Optional[bool] = None,
    ):
        if revoked is None:
            revoked = 0
        note = Token(
            user_id=user_id,
            device=device,
            token=token,
            revoked=revoked,
        )
        db.session.add(note)
        db.session.commit()


class DatabaseUpdater:
    def update_access_token(self): ...


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


if __name__ == "__main__":
    adder = DatabaseAdder()
    adder.add_user("nigger", "<EMAIL>", "<PASSWORD>")
    adder.add_tokens(1, "d", "ds", "fdsf")
