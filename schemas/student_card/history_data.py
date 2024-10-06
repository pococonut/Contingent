from pydantic import BaseModel


class HistoryDataSh(BaseModel):
    """
    Модель тела запроса об истории студента.
    """
    movements: str | None = None
    statuses: str | None = None

    personal_id: int | None = None

    class Config:
        orm_mode = True
        from_attributes = True
