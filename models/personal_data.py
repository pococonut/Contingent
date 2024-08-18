from __future__ import annotations

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.database import Base


class PersonalData(Base):
    """
    Модель таблицы личной информации студента.
    """
    __tablename__ = 'personal_data'

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    birth_date: Mapped[str] = mapped_column(nullable=True)
    birth_place: Mapped[str] = mapped_column(nullable=True)
    citizenship: Mapped[str] = mapped_column(nullable=True)
    type_of_identity: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    snils: Mapped[str] = mapped_column(nullable=True)
    polis: Mapped[str] = mapped_column(nullable=True)
    study_status: Mapped[str] = mapped_column(nullable=True)
    general_status: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)

    educational_data: Mapped["EducationalData"] = relationship("EducationalData", back_populates="personal_data",
                                                               uselist=False)
    contact_data: Mapped["ContactData"] = relationship("ContactData", back_populates="personal_data",
                                                       uselist=False)
    benefits_data: Mapped["BenefitsData"] = relationship("BenefitsData", back_populates="personal_data",
                                                         uselist=False)
    military_data: Mapped["MilitaryData"] = relationship("MilitaryData", back_populates="personal_data",
                                                          uselist=False)
    stipend_data: Mapped["StipendData"] = relationship("StipendData", back_populates="personal_data",
                                                       uselist=False)
    other_data: Mapped["OtherData"] = relationship("OtherData", back_populates="personal_data",
                                                   uselist=False)
