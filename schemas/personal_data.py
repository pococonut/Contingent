from pydantic import BaseModel


class PersonalDataSh(BaseModel):
    """
    Модель тела запроса информации студента.
    """
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    birth_date: str | None = None
    birth_place: str | None = None
    citizenship: str | None = None
    type_of_identity: str | None = None
    address: str | None = None
    snils: str | None = None
    polis: str | None = None
    study_status: str | None = None
    general_status: str | None = None
    genser: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True
