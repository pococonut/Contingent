from db.database import APIBase


class StipendDataSh(APIBase):
    """
    Модель тела запроса стипендии студента.
    """
    form: str | None = None
    amount: str | None = None
    personal_id: int | None = None

