from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List, Optional
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
    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # насчёт уникальности вопросики
    socket: Mapped[str] = mapped_column(String(20), nullable=False)
    core: Mapped[str] = mapped_column(String(5), nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    l2_cache: Mapped[str] = mapped_column(String(10), nullable=False)
    l3_cache: Mapped[str] = mapped_column(String(10), nullable=False)
    ddr4: Mapped[str] = mapped_column(String(10), nullable=False)
    ddr5: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    RAM_frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    TDP: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[str] = mapped_column(String(20), nullable=False)


class Motherboard(db.Model):
    __tablename__ = "motherboards"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    socket: Mapped[str] = mapped_column(String(20), nullable=False)
    chipset: Mapped[str] = mapped_column(String(20), nullable=False)
    RAM: Mapped[str] = mapped_column(String(10), nullable=False)
    RAM_frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    form_factor: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[str] = mapped_column(String(20), nullable=False)


class PowerUnit(db.Model):
    __tablename__ = "power_units"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    power: Mapped[str] = mapped_column(String(20), nullable=False)
    certificate: Mapped[str] = mapped_column(String(20), nullable=False)
    pin_cpu: Mapped[str] = mapped_column(String(20), nullable=False)
    pin_gpu: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[str] = mapped_column(String(20), nullable=False)


class Ram(db.Model):
    __tablename__ = "ram"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    volume: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[str] = mapped_column(String(20), nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    cl: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[str] = mapped_column(String(20), nullable=False)


class Ssd(db.Model):
    __tablename__ = "ssd"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    connector: Mapped[str] = mapped_column(String(20), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    interface: Mapped[str] = mapped_column(String(20), nullable=False)
    volume: Mapped[str] = mapped_column(String(20), nullable=False)
    sread: Mapped[str] = mapped_column(String(30), nullable=False)
    swrite: Mapped[str] = mapped_column(String(30), nullable=False)
    tbw: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[str] = mapped_column(String(20), nullable=False)


class VideoCard(db.Model):
    __tablename__ = "videocards"
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    PCIe: Mapped[str] = mapped_column(String(20), nullable=False)
    VRAM: Mapped[str] = mapped_column(String(20), nullable=False)
    type_VRAM: Mapped[str] = mapped_column(String(10), nullable=False)
    MIW: Mapped[str] = mapped_column(String(20), nullable=False)
    GPU_frequency: Mapped[str] = mapped_column(String(30), nullable=False)
    price: Mapped[str] = mapped_column(String(20), nullable=False)


COMPONENTS = {
    Processor.__tablename__: Processor,
    Motherboard.__tablename__: Motherboard,
    Ssd.__tablename__: Ssd,
    VideoCard.__tablename__: VideoCard,
    PowerUnit.__tablename__: PowerUnit,
    Ram.__tablename__: Ram,
}

# запретить доступ к login если есть токен в куках
