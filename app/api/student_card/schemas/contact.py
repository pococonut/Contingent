from db.database import APIBase


class ContactDataSh(APIBase):
    """
    Модель тела запроса контактной информации студента.
    """
    first_phone: str | None = None
    second_phone: str | None = None
    email: str | None = None
    personal_id: int


