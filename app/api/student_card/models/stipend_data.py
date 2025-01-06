from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from api.student_card.models.personal_data import PersonalData


class StipendData(Base):
    """
    Модель таблицы информации о стипендии студента.
    """
    __tablename__ = 'stipend_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    form: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(ForeignKey('personal_data.id'), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['personal_id'], ['personal_data.id'], ondelete='CASCADE'),)

    personal: Mapped["PersonalData"] = relationship("PersonalData", back_populates="stipend")

