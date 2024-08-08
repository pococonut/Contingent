from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base
from models.personal_data import PersonalData


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

    personal_data: Mapped["PersonalData"] = relationship("PersonalData", back_populates="other_data")

