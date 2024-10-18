from pydantic import BaseModel


class ProfileSh(BaseModel):
    """
    Схема профиля
    """
    name: str

