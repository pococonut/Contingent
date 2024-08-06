from pydantic import BaseModel


class OtherDataSh(BaseModel):
    """
    Модель тела запроса остальной информации студента.
    """
    parents: str | None = None
    parents_contacts: str | None = None
    relatives_works: str | None = None
    relatives_addresses: str | None = None
    personal_id: int


