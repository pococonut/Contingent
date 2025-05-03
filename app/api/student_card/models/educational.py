from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from api.student_card.models.personal import PersonalData


class EducationalData(Base):
    """
    Модель таблицы учебной деятельности студента.
    """
    __tablename__ = 'educational_data'
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
    study_duration: Mapped[str] = mapped_column(nullable=True)
    study_duration_total: Mapped[str] = mapped_column(nullable=True)
    study_profile: Mapped[str] = mapped_column(nullable=True)
    current_year: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


