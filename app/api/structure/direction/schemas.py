from db.database import APIBase


class DirectionSh(APIBase):
    """
    Схема направления
    """
    name: str
    short_name: str
    code: str
    courses: str
    qualification: str
    education_form: str

