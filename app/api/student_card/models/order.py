from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from api.student_card.models.personal import PersonalData


class OrderData(Base):
    """
    Модель таблицы информации о приказах.
    """
    __tablename__ = 'order_data'
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


