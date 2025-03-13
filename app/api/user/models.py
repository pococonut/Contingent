from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Boolean, LargeBinary

from db.database import Base


class User(Base):
    """
    Таблица данных пользователя
    """
    __tablename__ = 'user'
    __table_args__ = {'schema': 'test'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, unique=True, nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    access_token: Mapped[str] = mapped_column(nullable=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)

