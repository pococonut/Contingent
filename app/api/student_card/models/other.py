from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class OtherData(Base):
    """
    Модель таблицы об остальной информации студента.
    """
    __tablename__ = 'other_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_parent: Mapped[str] = mapped_column(nullable=True)
    second_parent: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


