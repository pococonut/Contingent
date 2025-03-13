from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from api.student_card.models.personal_data import PersonalData


class HistoryData(Base):
    """
    Модель таблицы информации об истории студента
    """
    __tablename__ = 'history_data'
    __table_args__ = {'schema': 'test'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    movements: Mapped[str] = mapped_column(nullable=True)
    statuses: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)

