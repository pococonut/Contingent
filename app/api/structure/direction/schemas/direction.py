from db.database import APIBase


class DirectionIn(APIBase):
    """
    Входная схема направления
    """
    name: str
    short_name: str
    code: str
    courses: str
    qualification: str
    education_form: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Математика и Компьютерные науки",
                    "short_name": "МиКН",
                    "code": "02.03.01",
                    "courses": "4",
                    "qualification": "Математика и Компьютерные науки",
                    "education_form": "очная"
                }
            ]
        }
    }


class DirectionOut(APIBase):
    """
    Выходная схема направления
    """
    id: int
    name: str
    short_name: str
    code: str
    courses: str
    qualification: str
    education_form: str