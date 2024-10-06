from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base
from models.student_card.personal_data import PersonalData


class OrderData(Base):
    """
    Модель таблицы информации о приказах.
    """
    __tablename__ = 'order_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(ForeignKey('personal_data.id'), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['personal_id'], ['personal_data.id'], ondelete='CASCADE'),)

    personal: Mapped["PersonalData"] = relationship("PersonalData", back_populates="order")

