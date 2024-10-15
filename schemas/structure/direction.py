from pydantic import BaseModel


class DirectionSh(BaseModel):
    """
    Схема направления
    """
    name: str
    short_name: str
    number: str
    courses: str
    qualification: str
    form: str

