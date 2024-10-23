from pydantic import BaseModel


class SubgroupSh(BaseModel):
    """
    Схема подгруппы
    """
    direction_name: str
    course: str
    department_name: str
    group_name: str
    profile_name: str
    name: list[str]

