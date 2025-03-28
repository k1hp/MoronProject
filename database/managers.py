from database.creation import db, Base, User, Token
from typing import Optional


class DatabaseManager:
    def create_all(self):
        ...

    def drop_all(self):
        ...

    def drop_table(self, table: Base) -> None:
        ...


class DatabaseAdder:
    def add_all(self):
        ...

    def add_user(self, login: str, email: str, password: str) -> None:
        user = User(login=login, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    def add_tokens(self, user_id: int, device: str, access_token: str, refresh_token: str, revoked: Optional[bool] = None):
        if revoked is None:
            revoked = 0
        note = Token(user_id=user_id, device=device, access_token=access_token, refresh_token=refresh_token, revoked=revoked )
        db.session.add(note)
        db.session.commit()

class DatabaseUpdater:
    def update_access_token(self):
        ...


if __name__ == '__main__':
    adder = DatabaseAdder()
    adder.add_user("nigger", "<EMAIL>", "<PASSWORD>")
    adder.add_tokens(1, "d", "ds", "fdsf")