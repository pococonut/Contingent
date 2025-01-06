from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class SubgroupData(Base):
    """
    Модель таблицы подгрупп
    """
    __tablename__ = "subgroup"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[str] = mapped_column(nullable=True)
    department: Mapped[str] = mapped_column(nullable=True)
    group: Mapped[str] = mapped_column(nullable=True)
    profile: Mapped[str] = mapped_column(nullable=True)
    subgroup: Mapped[str] = mapped_column(nullable=True)



