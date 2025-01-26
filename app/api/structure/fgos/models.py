from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class FgosData(Base):
    """
    Модель таблицы ФГОСов
    """
    __tablename__ = "fgos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)


