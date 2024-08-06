from pydantic import BaseModel


class StipendDataSh(BaseModel):
    """
    Модель тела запроса о стипендии студента.
    """
    form: str | None = None
    amount: str | None = None
    personal_id: int

