from db.database import APIBase


class FgosIn(APIBase):
    """
    Схема ФГОСа
    """
    name: str


class FgosOut(APIBase):
    """
    Схема ФГОСа
    """
    id: int
    name: str
