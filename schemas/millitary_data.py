from pydantic import BaseModel


class MilitaryDataSh(BaseModel):
    """
    Модель тела запроса об отношении к военной службе студента.
    """
    status: str | None = None
    category: str | None = None
    delay: str | None = None
    document: str | None = None
    personal_id: int

