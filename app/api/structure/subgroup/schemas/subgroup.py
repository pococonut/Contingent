from db.database import APIBase


class SubgroupIn(APIBase):
    """
    Входная схема подгруппы
    """
    department: str
    group: str
    profile: str
    subgroup: list[str]


class SubgroupOut(APIBase):
    """
    Выходная схема подгруппы
    """
    id: int
    department: str
    group: str
    profile: str
    subgroup: list[str] | str

