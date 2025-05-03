from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class PersonalData(Base):
    """
    Модель таблицы личной информации студента.
    """
    __tablename__ = 'personal_data'
    

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    birth_date: Mapped[str] = mapped_column(nullable=True)
    birth_place: Mapped[str] = mapped_column(nullable=True)
    citizenship: Mapped[str] = mapped_column(nullable=True)
    type_of_identity: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    snils: Mapped[str] = mapped_column(nullable=True)
    polis: Mapped[str] = mapped_column(nullable=True)
    study_status: Mapped[str] = mapped_column(nullable=True)
    general_status: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)

