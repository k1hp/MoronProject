from database.creation import db, User
from app.others.settings import DB_CONNECTION
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from typing import List

engine = create_engine(DB_CONNECTION)
Session = sessionmaker(bind=engine)


def add_many(data: List[dict], table: db.Model):
    with Session() as session:
        session.execute(insert(table), data)
        session.commit()


if __name__ == "__main__":
    add_many(
        data=[{"login": "fdsafd", "email": "41212@gmail.com", "password": "12345"}],
        table=User,
    )
