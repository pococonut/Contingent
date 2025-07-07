from db.database import APIBase


class FgosIn(APIBase):
    """
    Входная схема ФГОСа
    """
    name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "3++"
                }
            ]
        }
    }


class FgosOut(APIBase):
    """
    Выходная схема ФГОСа
    """
    id: int
    name: str
