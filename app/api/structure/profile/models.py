from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from db.database import Base
import db_config


class ProfileData(Base):
    """
    Модель таблицы профилей
    """
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(db_config.MAX_LEN_PROFILE_NAME), unique=True, nullable=True)
    short_name: Mapped[str] = mapped_column(String(db_config.MAX_LEN_PROFILE_SHORT_NAME), unique=True, nullable=True)


