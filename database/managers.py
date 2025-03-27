from database.creation import db, Base, User


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

    def add_tokens(self):
        ...