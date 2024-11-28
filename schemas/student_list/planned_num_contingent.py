from db.database import APIBase


class PlannedNumContingentSh(APIBase):
    """
    Модель запроса планируемого численного списка студентов
    """
    direction: str
    course: str
    groups: str
    subgroups: str
