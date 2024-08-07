from pydantic import BaseModel


class ContactDataSh(BaseModel):
    """
    Модель тела запроса контактной информации студента.
    """
    number: str | None = None
    spare_number: str | None = None
    mail: str | None = None
    personal_id: int | None = None

    class Config:
        orm_mode = True
        from_attributes = True

