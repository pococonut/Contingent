from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base
from models.personal_data import PersonalData


class ContactData(Base):
    """
    Модель таблицы контактной информации студента.
    """
    __tablename__ = 'contact_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(nullable=True)
    spare_number: Mapped[str] = mapped_column(nullable=True)
    mail: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(ForeignKey('personal_data.personal_id'), nullable=False)

    personal_data: Mapped["PersonalData"] = relationship("PersonalData", back_populates="contact_data")

