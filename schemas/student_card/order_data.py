from db.database import APIBase


class OrderDataSh(APIBase):
    """
    Модель тела запроса о приказах.
    """
    order: str | None = None
    personal_id: int | None = None

