from pydantic import BaseModel


class FgosSh(BaseModel):
    """
    Схема ФГОСа
    """
    name: str

