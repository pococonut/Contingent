from db.database import APIBase


class ShortCard(APIBase):
    """
    Модель тела запроса сокращенной карты студента.
    """
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    direction: str | None = None
    course: str | None = None
    department: str | None = None
    group: str | None = None
    subgroup: str | None = None


