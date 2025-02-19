from db.database import APIBase
    

class UserSchema(APIBase):
    """
    Схема данных пользователя
    """
    first_name: str
    last_name: str
    middle_name: str | None = None
    login: str
    password: bytes
    role: str
    active: bool | None = None
    access_token: str | None = None
    refresh_token: str | None = None


class UserSchemaOut(APIBase):
    """
    Схема ответа для данных пользователя
    """
    first_name: str
    last_name: str
    middle_name: str | None = None
    role: str
