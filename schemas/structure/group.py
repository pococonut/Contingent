from pydantic import BaseModel


class GroupSh(BaseModel):
    """
    Схема направления
    """
    direction_name: str
    course: str
    name: list[str]

