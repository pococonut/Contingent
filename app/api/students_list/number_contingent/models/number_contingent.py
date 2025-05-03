from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class PlannedNumContingent(Base):
    """
    Модель таблицы планируемого численного списка студентов
    """
    __tablename__ = 'planned_num_contingent'
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction: Mapped[str] = mapped_column(nullable=False)
    course: Mapped[int] = mapped_column(nullable=False)
    groups: Mapped[int] = mapped_column(nullable=False)
    subgroups: Mapped[int] = mapped_column(nullable=False)
