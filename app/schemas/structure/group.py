from db.database import APIBase


class GroupSh(APIBase):
    """
    Схема направления
    """
    direction_name: str
    course: str
    fgos: str
    name: list[str]

