from db.database import APIBase


class ProfileIn(APIBase):
    """
    Схема профиля
    """
    name: str
    short_name: str


class ProfileOut(APIBase):
    """
    Схема профиля
    """
    id: int
    name: str
    short_name: str

