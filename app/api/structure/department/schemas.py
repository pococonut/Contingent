from db.database import APIBase


class DepartmentIn(APIBase):
    """
    Входная схема кафедры
    """
    name: str
    short_name: str


class DepartmentOut(APIBase):
    """
    Выходная схема кафедры
    """
    id: int
    name: str
    short_name: str
