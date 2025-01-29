from db.database import APIBase


class SubgroupIn(APIBase):
    """
    Схема подгруппы
    """
    department: str
    group: str
    profile: str
    subgroup: list[str]


class SubgroupOut(APIBase):
    """
    Схема подгруппы
    """
    id: int
    department: str
    group: str
    profile: str
    subgroup: list[str] | str

