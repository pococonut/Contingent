from pydantic import BaseModel


class DepartmentSh(BaseModel):
    """
    Схема кафедры
    """
    name: str
    short_name: str

