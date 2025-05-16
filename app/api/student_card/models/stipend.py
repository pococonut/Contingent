from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class StipendData(Base):
    """
    Модель таблицы информации о стипендии студента.
    """
    __tablename__ = 'stipend_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    academic: Mapped[str] = mapped_column(nullable=True)
    social: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


