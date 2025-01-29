from db.database import APIBase


class DepartmentIn(APIBase):
    """
    Схема кафедры
    """
    name: str
    short_name: str


class DepartmentOut(APIBase):
    """
    Схема кафедры
    """
    id: int
    name: str
    short_name: str
