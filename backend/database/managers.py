from backend.database.creation import db, User
from backend.app.services.helpers import Password
from backend.app.others.settings import DB_CONNECTION, DB_NAME
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from typing import List

engine = create_engine(DB_CONNECTION + DB_NAME)
Session = sessionmaker(bind=engine)


def add_many(data: List[dict], table: db.Model):
    with Session() as session:
        session.execute(insert(table), data)
        session.commit()


if __name__ == "__main__":
    add_many(
        data=[
            {
                "email": "41212@gmail.com",
                "password": Password("12345").hash,
            }
        ],
        table=User,
    )
