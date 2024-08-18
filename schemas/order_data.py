from pydantic import BaseModel


class OrderDataSh(BaseModel):
    """
    Модель тела запроса о приказах.
    """
    order: str | None = None
    personal_id: int | None = None

    class Config:
        orm_mode = True
        from_attributes = True
