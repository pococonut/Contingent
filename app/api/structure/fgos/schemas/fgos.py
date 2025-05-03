from db.database import APIBase


class FgosIn(APIBase):
    """
    Входная схема ФГОСа
    """
    name: str


class FgosOut(APIBase):
    """
    Выходная схема ФГОСа
    """
    id: int
    name: str
