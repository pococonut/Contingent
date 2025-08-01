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
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    photo: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    birth: Mapped[str] = mapped_column(String(50), nullable=True)
    structure: Mapped[str] = mapped_column(String(100), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    access_token: Mapped[str] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)

