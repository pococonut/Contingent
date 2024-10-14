from pydantic import BaseModel


class ProfileSh(BaseModel):
    """
    Схема профиля
    """
    profile: str

