from pydantic import BaseModel


class PersonalDataSh(BaseModel):
    """
    Модель тела запроса информации студента.
    """
    personal_id: int
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    birth_date: str | None = None
    birth_place: str | None = None
    citizenship: str | None = None
    type_of_identity: str | None = None
    address: str | None = None
    marital_status: str | None = None
    snils: str | None = None
    polis: str | None = None
    study_status: str | None = None
    general_status: str | None = None
