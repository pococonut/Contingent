from pydantic import BaseModel


class SubgroupSh(BaseModel):
    """
    Схема подгруппы
    """
    direction: str
    course: str
    group: str
    profile: str
    subgroup: list[str]

