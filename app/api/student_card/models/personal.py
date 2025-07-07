from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class PersonalData(Base):
    """
    Модель таблицы личной информации студента.
    """
    __tablename__ = 'personal_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    birth: Mapped[str] = mapped_column(nullable=False)
    place_of_birth: Mapped[str] = mapped_column(nullable=True)
    citizenship: Mapped[str] = mapped_column(nullable=True)
    identity_cards: Mapped[str] = mapped_column(nullable=True)
    residential_address: Mapped[str] = mapped_column(nullable=True)
    registration_address: Mapped[str] = mapped_column(nullable=True)
    snils: Mapped[str] = mapped_column(nullable=True)
    global_status: Mapped[str] = mapped_column(nullable=False)
    inner_status: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)

