from db.database import APIBase


class SubgroupSh(APIBase):
    """
    Схема подгруппы
    """
    department: str
    group: str
    profile: str
    subgroup: list[str]

