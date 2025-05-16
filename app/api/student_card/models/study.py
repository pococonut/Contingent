from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class StudyData(Base):
    """
    Модель таблицы учебной деятельности студента.
    """
    __tablename__ = 'study_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    faculty: Mapped[str] = mapped_column(nullable=False)
    course: Mapped[str] = mapped_column(nullable=False)
    direction: Mapped[str] = mapped_column(nullable=False)
    group: Mapped[str] = mapped_column(nullable=False)
    subgroup: Mapped[str] = mapped_column(nullable=False)
    educational_form: Mapped[str] = mapped_column(nullable=False)
    degree_of_study: Mapped[str] = mapped_column(nullable=False)
    learning_conditions: Mapped[str] = mapped_column(nullable=False)
    department: Mapped[str] = mapped_column(nullable=True)
    profile: Mapped[str] = mapped_column(nullable=True)
    record_book_number: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[str] = mapped_column(nullable=False)
    end_date: Mapped[str] = mapped_column(nullable=False)
    period_of_study: Mapped[str] = mapped_column(nullable=True)
    stipend_academic: Mapped[str] = mapped_column(nullable=True)
    stipend_social: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


