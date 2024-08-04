from pydantic import BaseModel


class ShortCard(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    direction: str | None = None
    course: str | None = None
    department: str | None = None
    group: str | None = None
    subgroup: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True

