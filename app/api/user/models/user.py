from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Boolean, LargeBinary

from db.database import Base


class User(Base):
    """
    Таблица данных пользователя
    """
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    short_name: Mapped[str] = mapped_column(String(50), nullable=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    password: Mapped[bytes] = mapped_column(String, nullable=True)
    photo: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=True)
    birth: Mapped[str] = mapped_column(String(50), nullable=True)
    structure: Mapped[str] = mapped_column(String(100), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    access_token: Mapped[str] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)

