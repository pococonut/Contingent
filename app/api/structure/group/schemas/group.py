from db.database import APIBase


class GroupIn(APIBase):
    """
    Входная схема направления
    """
    direction: str
    course: str
    fgos: str
    group: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "direction": "Математика и Компьютерные науки",
                    "course": "1",
                    "fgos": "3++",
                    "group": [
                        "11", "12", "13"
                    ]
                }
            ]
        }
    }

class GroupOut(APIBase):
    """
    Выходная схема направления
    """
    id: int
    direction: str
    course: str
    fgos: str
    group: list[str] | str

