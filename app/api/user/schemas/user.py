from fastapi import UploadFile
from pydantic import EmailStr

from db.database import APIBase


class UserSchema(APIBase):
    """
    Схема данных пользователя
    """
    first_name: str
    last_name: str
    middle_name: str | None = None
    short_name: str | None = None
    login: str
    password: bytes
    email: EmailStr | None = None
    active: bool | None = True
    birth: str | None = None
    structure: str | None = None
    gender: str | None = None
    role: str
    # access_token: str | None = None
    # refresh_token: str | None = None

    """@field_serializer("password")
    def serialize_password(self, password: bytes, _info):
        return hash_password(password)"""


class UserSchemaOut(APIBase):
    """
    Схема ответа для данных пользователя
    """
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None
    short_name: str | None = None
    login: str
    password: bytes
    photo: str | None = None
    email: EmailStr | None = None
    active: bool | None = True
    birth: str | None = None
    structure: str | None = None
    gender: str | None = None
    role: str


class UserFullName(APIBase):
    """
    Схема полного имени пользователя
    """
    first_name: str
    last_name: str
    middle_name: str | None = None
