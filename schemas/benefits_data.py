from pydantic import BaseModel


class BenefitsDataSh(BaseModel):
    """
    Модель тела запроса о льготах студента.
    """
    benefits: str | None = None
    personal_id: int | None = None

    class Config:
        orm_mode = True
        from_attributes = True
