from db.database import APIBase


class ProfileIn(APIBase):
    """
    Входная схема профиля
    """
    name: str
    short_name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Математика",
                    "short_name": "М"
                }
            ]
        }
    }


class ProfileOut(APIBase):
    """
    Выходная схема профиля
    """
    id: int
    name: str
    short_name: str

