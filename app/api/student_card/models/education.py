from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class EducationData(Base):
    """
    Модель таблицы образования студента.
    """
    __tablename__ = 'education_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    educational_document: Mapped[str] = mapped_column(nullable=True)
    document_serial_number: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


