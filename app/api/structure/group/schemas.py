from db.database import APIBase


class GroupSh(APIBase):
    """
    Схема направления
    """
    direction: str
    course: str
    fgos: str
    group: list[str]

