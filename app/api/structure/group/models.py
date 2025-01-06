from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class GroupData(Base):
    """
    Модель таблицы групп
    """
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    direction: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[str] = mapped_column(nullable=True)
    fgos: Mapped[str] = mapped_column(nullable=True)
    group: Mapped[str] = mapped_column(nullable=True)


