from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from db.database import Base
import db_config


class SubgroupData(Base):
    """
    Модель таблицы подгрупп
    """
    __tablename__ = "subgroup"
    __table_args__ = {'schema': 'test'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    department: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DEPARTMENT_NAME), nullable=True)  # 200
    group: Mapped[str] = mapped_column(String(db_config.MAX_LEN_GROUP_NAME), nullable=True)  # 50
    profile: Mapped[str] = mapped_column(String(db_config.MAX_LEN_PROFILE_NAME), nullable=True)  # 200
    subgroup: Mapped[str] = mapped_column(String(db_config.MAX_LEN_SUBGROUP_NAME), unique=True, nullable=True)  # 50



