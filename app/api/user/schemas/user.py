from pydantic import field_validator

from db.database import APIBase


class UserSchema(APIBase):
    """
    Схема данных пользователя
    """
    first_name: str
    last_name: str
    middle_name: str | None = None
    login: str
    password: str
    phone: str
    email: str | None = None
    birth: str | None = None
    structure: str | None = None
    gender: str
    role: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Полина",
                    "last_name": "Золотухина",
                    "middle_name": "Викторовна",
                    "login": "po",
                    "password": "string",
                    "phone": "88005353535",
                    "email": "po@mail.ru",
                    "birth": "16.09.2003",
                    "structure": "нет",
                    "gender": "ж",
                    "role": "admin"
                }
            ]
        }
    }

    @field_validator('first_name', 'last_name', 'middle_name', mode='before')
    @classmethod
    def capitalize_parameter(cls, value):
        if isinstance(value, str) and value:
            return value.capitalize()
        return value

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
    password: str
    phone: str
    email: str | None = None
    birth: str | None = None
    structure: str | None = None
    gender: str
    role: str


class UserFullName(APIBase):
    """
    Схема полного имени пользователя
    """
    first_name: str
    last_name: str
    middle_name: str | None = None
