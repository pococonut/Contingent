from db.database import APIBase


class HistoryDataSh(APIBase):
    """
    Модель тела запроса об истории студента.
    """
    movements: str | None = None
    statuses: str | None = None

    personal_id: int | None = None

