from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base
from models.personal_data import PersonalData


class EducationalData(Base):
    """
    Модель таблицы учебной деятельности студента.
    """
    __tablename__ = 'educational_data'

    education_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    faculty: Mapped[str] = mapped_column(nullable=True)
    direction: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[str] = mapped_column(nullable=True)
    department: Mapped[str] = mapped_column(nullable=True)
    group: Mapped[str] = mapped_column(nullable=True)
    subgroup: Mapped[str] = mapped_column(nullable=True)
    form: Mapped[str] = mapped_column(nullable=True)
    book_num: Mapped[str] = mapped_column(nullable=True)
    degree: Mapped[str] = mapped_column(nullable=True)
    degree_payment: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(ForeignKey('personal_data.personal_id'), nullable=False)

    personal_data: Mapped["PersonalData"] = relationship("PersonalData", back_populates="educational_data")

