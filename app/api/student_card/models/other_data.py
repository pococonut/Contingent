from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from api.student_card.models.personal_data import PersonalData


class OtherData(Base):
    """
    Модель таблицы об остальной информации студента.
    """
    __tablename__ = 'other_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parents: Mapped[str] = mapped_column(nullable=True)
    parents_contacts: Mapped[str] = mapped_column(nullable=True)
    relatives_works: Mapped[str] = mapped_column(nullable=True)
    relatives_addresses: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(ForeignKey('personal_data.id'), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['personal_id'], ['personal_data.id'], ondelete='CASCADE'),)

    personal: Mapped["PersonalData"] = relationship("PersonalData", back_populates="other")

