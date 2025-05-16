from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class BenefitsData(Base):
    """
    Модель таблицы информации о льготах студента.
    """
    __tablename__ = 'benefits_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    benefits_type: Mapped[str] = mapped_column(nullable=True)

    personal_id: Mapped[int] = mapped_column(nullable=False)


