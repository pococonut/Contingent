from db.database import APIBase


class GroupIn(APIBase):
    """
    Схема направления
    """
    direction: str
    course: str
    fgos: str
    group: list[str]


class GroupOut(APIBase):
    """
    Схема направления
    """
    id: int
    direction: str
    course: str
    fgos: str
    group: list[str] | str

