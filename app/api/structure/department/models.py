from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base
import db_config


class DepartmentData(Base):
    """
    Модель таблицы кафедр
    """
    __tablename__ = "department"
    __table_args__ = {'schema': 'test'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DEPARTMENT_NAME), unique=True, nullable=True)
    short_name: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DEPARTMENT_SHORT_NAME), unique=True, nullable=True)


