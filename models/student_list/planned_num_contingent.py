from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class PlannedNumContingent(Base):
    """
    Модель таблицы планируемого численного списка студентов
    """
    __tablename__ = 'planned_num_contingent'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction: Mapped[str] = mapped_column(nullable=False)
    course: Mapped[str] = mapped_column(nullable=False)
    free: Mapped[str] = mapped_column(nullable=False)
    contract: Mapped[str] = mapped_column(nullable=False)
    groups: Mapped[str] = mapped_column(nullable=False)
    subgroups: Mapped[str] = mapped_column(nullable=False)
