from db.database import APIBase


class DirectionIn(APIBase):
    """
    Входная схема направления
    """
    name: str
    short_name: str
    code: str
    courses: str
    qualification: str
    education_form: str


class DirectionOut(APIBase):
    """
    Выходная схема направления
    """
    id: int
    name: str
    short_name: str
    code: str
    courses: str
    qualification: str
    education_form: str