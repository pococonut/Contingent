from db.database import APIBase


class OtherDataSh(APIBase):
    """
    Модель тела запроса остальной информации студента.
    """
    first_parent: str | None = None
    second_parent: str | None = None
    personal_id: int



