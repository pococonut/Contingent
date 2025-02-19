from db.database import APIBase


class TokenInfo(APIBase):
    """
    Схема данных пользователя
    """
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"

