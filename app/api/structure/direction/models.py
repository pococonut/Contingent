from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from db.database import Base
import db_config


class DirectionData(Base):
    """
    Модель таблицы направлений
    """
    __tablename__ = "direction"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_NAME), unique=True, nullable=True)
    short_name: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_SHORT_NAME), unique=True, nullable=True)
    code: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_CODE), unique=True, nullable=True)
    courses: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_COURSES), nullable=True)
    qualification: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_QUALIFICATION), nullable=True)
    education_form: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_EDUCATION_FORM), nullable=True)

