from db.database import APIBase


class ProfileSh(APIBase):
    """
    Схема профиля
    """
    name: str
    short_name: str


