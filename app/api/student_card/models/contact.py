from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class ContactData(Base):
    """
    Модель таблицы контактной информации студента.
    """
    __tablename__ = 'contact_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_phone: Mapped[str] = mapped_column(nullable=True)
    second_phone: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


