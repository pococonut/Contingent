from db.database import APIBase


class StructureOut(APIBase):
    """
    Схема Структуры
    """
    id: int
    subgroup: str
    profile: str
    group: str
    course: str
    direction: str
    code: str
    qualification: str
    education_form: str


