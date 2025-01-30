from db.database import APIBase


class ProfileIn(APIBase):
    """
    Входная схема профиля
    """
    name: str
    short_name: str


class ProfileOut(APIBase):
    """
    Выходная схема профиля
    """
    id: int
    name: str
    short_name: str

