from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

from db.database import Base
import db_config


class GroupData(Base):
    """
    Модель таблицы групп
    """
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_NAME),
                                           ForeignKey('direction.name', onupdate='CASCADE'),
                                           nullable=True)
    course: Mapped[str] = mapped_column(String(db_config.MAX_LEN_DIRECTION_COURSES), nullable=True)
    fgos: Mapped[str] = mapped_column(String(db_config.MAX_LEN_FGOS_NAME), nullable=True)
    group: Mapped[str] = mapped_column(String(db_config.MAX_LEN_GROUP_NAME), unique=True, nullable=True)

    subgroups: Mapped[list["SubgroupData"]] = relationship(back_populates="group_rel")
    # Отношение для доступа к родительскому объекту
    direction_rel: Mapped["DirectionData"] = relationship(back_populates="groups")

