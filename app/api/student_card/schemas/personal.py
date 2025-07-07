from db.database import APIBase


class PersonalDataShIn(APIBase):
    """
    Модель тела запроса информации студента.
    """
    first_name: str
    last_name: str
    middle_name: str | None = None
    birth: str
    place_of_birth: str | None = None
    citizenship: str | None = None
    identity_cards: str | None = None
    residential_address: str | None = None
    registration_address: str | None = None
    snils: str | None = None
    global_status: str
    inner_status: str
    gender: str


class PersonalDataShOut(PersonalDataShIn):
    id: int

