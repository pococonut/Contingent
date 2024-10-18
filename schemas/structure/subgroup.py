from pydantic import BaseModel


class SubgroupSh(BaseModel):
    """
    Схема подгруппы
    """
    direction_name: str
    course: str
    group_name: str
    profile_name: str
    name: list[str]

