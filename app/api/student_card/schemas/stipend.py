from db.database import APIBase


class StipendDataSh(APIBase):
    """
    Модель тела запроса стипендии студента.
    """
    academic: str | None = None
    social: str | None = None
    personal_id: int

