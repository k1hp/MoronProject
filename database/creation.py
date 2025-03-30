from xmlrpc.client import Boolean

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List
from datetime import date, datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    login: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="user")


class Token(
    db.Model
):  # удаленные токены потом в планировщике будем удалять, а так статус revoked false ставим
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    device: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    token: Mapped[str] = mapped_column(
        String(130), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    revoked: Mapped[bool] = mapped_column(nullable=False, index=True, default=False)

    user: Mapped[User] = relationship("User", back_populates="tokens")
