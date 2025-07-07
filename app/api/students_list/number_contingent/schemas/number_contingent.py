from db.database import APIBase


class PlannedNumContingentSh(APIBase):
    """
    Модель запроса планируемого численного списка студентов
    """
    direction: str
    course: int
    groups: int
    subgroups: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "direction": "Математика и компьютерные науки",
                    "course": 2,
                    "groups": 3,
                    "subgroups": 6
                }
            ]
        }
    }