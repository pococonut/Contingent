from db.database import APIBase


class SubgroupSh(APIBase):
    """
    Схема подгруппы
    """
    direction: str
    course: str
    department: str
    group: str
    profile: str
    subgroup: list[str]

