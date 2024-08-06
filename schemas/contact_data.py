from pydantic import BaseModel


class ContactDataSh(BaseModel):
    """
    Модель тела запроса контактной информации студента.
    """
    number: str | None = None
    spare_number: str | None = None
    mail: str | None = None
    personal_id: int

