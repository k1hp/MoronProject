from database.creation import db, Base
class DatabaseManager:
    def create_all(self):
        ...

    def drop_all(self):
        ...

    def drop_table(self, table: Base) -> None:
        # db.drop_all(tables=[table.__table__])
        ...
