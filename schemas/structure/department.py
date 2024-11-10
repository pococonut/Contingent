from db.database import APIBase


class DepartmentSh(APIBase):
    """
    Схема кафедры
    """
    name: str
    short_name: str

