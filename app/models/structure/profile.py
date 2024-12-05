from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class ProfileData(Base):
    """
    Модель таблицы профилей
    """
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)


