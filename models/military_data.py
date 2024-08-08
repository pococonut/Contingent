from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base
from models.personal_data import PersonalData


class MilitaryData(Base):
    """
    Модель таблицы информации об отношении к военной службе студента.
    """
    __tablename__ = 'military_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=True)
    delay: Mapped[str] = mapped_column(nullable=True)
    document: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(ForeignKey('personal_data.personal_id'), nullable=False)

    personal_data: Mapped["PersonalData"] = relationship("PersonalData", back_populates="military_data")

