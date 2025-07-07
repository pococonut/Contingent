from db.database import APIBase


class DepartmentIn(APIBase):
    """
    Входная схема кафедры
    """
    name: str
    short_name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Вычислительная математика и компьютерные науки",
                    "short_name": "ВМИ"
                }
            ]
        }
    }


class DepartmentOut(APIBase):
    """
    Выходная схема кафедры
    """
    id: int
    name: str
    short_name: str
