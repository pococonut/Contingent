from db.database import APIBase


class MilitaryDataSh(APIBase):
    """
    Модель тела запроса об отношении к военной службе студента.
    """
    status: str | None = None
    category: str | None = None
    deferment_end_date: str | None = None
    document: str | None = None
    personal_id: int

