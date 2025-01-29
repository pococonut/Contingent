from db.database import APIBase


class DirectionIn(APIBase):
    """
    Схема направления
    """
    name: str
    short_name: str
    code: str
    courses: str
    qualification: str
    education_form: str


class DirectionOut(APIBase):
    """
    Схема направления
    """
    id: int
    name: str
    short_name: str
    code: str
    courses: str
    qualification: str
    education_form: str