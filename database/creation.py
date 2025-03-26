from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    

