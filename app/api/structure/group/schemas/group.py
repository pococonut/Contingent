from db.database import APIBase


class GroupIn(APIBase):
    """
    Входная схема направления
    """
    direction: str
    course: str
    fgos: str
    group: list[str]


class GroupOut(APIBase):
    """
    Выходная схема направления
    """
    id: int
    direction: str
    course: str
    fgos: str
    group: list[str] | str

