from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class DirectionData(Base):
    """
    Модель таблицы направлений
    """
    __tablename__ = "direction"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    short_name: Mapped[str] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(nullable=True)
    courses: Mapped[str] = mapped_column(nullable=True)
    qualification: Mapped[str] = mapped_column(nullable=True)
    education_form: Mapped[str] = mapped_column(nullable=True)

