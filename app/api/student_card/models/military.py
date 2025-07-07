from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class MilitaryData(Base):
    """
    Модель таблицы информации об отношении к военной службе студента.
    """
    __tablename__ = 'military_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=True)
    deferment_end_date: Mapped[str] = mapped_column(nullable=True)
    document: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


