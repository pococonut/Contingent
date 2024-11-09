from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    """
    Схема данных пользователя
    """
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool | None = True


class TokenInfo(BaseModel):
    """
    Схема данных пользователя
    """
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"

