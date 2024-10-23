from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.database import Base


class SubgroupData(Base):
    """
    Модель таблицы подгрупп
    """
    __tablename__ = "subgroup"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction_name: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[str] = mapped_column(nullable=True)
    department_name: Mapped[str] = mapped_column(nullable=True)
    group_name: Mapped[str] = mapped_column(nullable=True)
    profile_name: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)



