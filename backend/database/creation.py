from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List
from datetime import date, datetime, timedelta


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    token: Mapped["Token"] = relationship("Token", back_populates="user")
    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")


class Profile(db.Model):
    __tablename__ = "profiles"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, primary_key=True
    )
    nickname: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    photo_link: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
        default="https://i1.sndcdn.com/artworks-b8vZs1TN28AFyDpi-JHQM6w-t1080x1080.png",
    )
    status: Mapped[str] = mapped_column(String(80), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="profile")


class Token(
    db.Model
):  # удаленные токены потом в планировщике будем удалять, а так статус revoked false ставим
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(
        String(130), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    expired_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now() + timedelta(days=15)
    )
    # expired_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())

    user: Mapped[User] = relationship("User", back_populates="token")


class Processor(db.Model):
    __tablename__ = "processors"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    socket: Mapped[str] = mapped_column(String(10), nullable=False)
    core: Mapped[str] = mapped_column(String(5), nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    l2_cache: Mapped[str] = mapped_column(String(10), nullable=False)
    l3_cache: Mapped[str] = mapped_column(String(10), nullable=False)
    ddr4: Mapped[str] = mapped_column(String(20), nullable=False)
    ddr5: Mapped[str] = mapped_column(String(20))
    RAM_frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    TDP: Mapped[str] = mapped_column(String(20), nullable=False)
    # price: Mapped[int] = mapped_column(nullable=False)


# запретить доступ к login если есть токен в куках
