from db.database import APIBase


class SubgroupIn(APIBase):
    """
    Входная схема подгруппы
    """
    department: str
    group: str
    profile: str
    subgroup: list[str]

    model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "department": "Вычислительная математика и информатика",
                        "group": "11",
                        "profile": "Математика",
                        "subgroup": [
                            "11/1", "11/2"
                        ]
                    }
                ]
            }
        }

class SubgroupOut(APIBase):
    """
    Выходная схема подгруппы
    """
    id: int
    department: str
    group: str
    profile: str
    subgroup: list[str] | str

