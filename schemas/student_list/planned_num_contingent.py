from db.database import APIBase


class PlannedNumContingentSh(APIBase):
    """
    Модель запроса планируемого численного списка студентов
    """
    direction: str
    course: str
    free: str
    contract: str
    groups: str
    subgroups: str
