from pydantic import BaseModel


class GroupSh(BaseModel):
    """
    Схема направления
    """
    direction: str
    course: str
    fgos: str
    group: str

