from db.database import APIBase


class DirectionSh(APIBase):
    """
    Схема направления
    """
    name: str
    short_name: str
    number: str
    courses: str
    qualification: str
    form: str

