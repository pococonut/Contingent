from pydantic import EmailStr

from db.database import APIBase


class TokenInfo(APIBase):
    """
    Схема данных пользователя
    """
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserSchemaAuth(APIBase):
    """
    Схема данных пользователя
    """
    login: str
    password: bytes
    email: EmailStr | None = None
    active: bool | None = True
