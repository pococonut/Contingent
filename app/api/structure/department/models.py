from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class DepartmentData(Base):
    """
    Модель таблицы кафедр
    """
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)
    short_name: Mapped[str] = mapped_column(unique=True, nullable=True)


