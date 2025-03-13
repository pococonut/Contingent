from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from db.database import Base
import db_config


class FgosData(Base):
    """
    Модель таблицы ФГОСов
    """
    __tablename__ = "fgos"
    __table_args__ = {'schema': 'test'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(db_config.MAX_LEN_FGOS_NAME), unique=True, nullable=True)


