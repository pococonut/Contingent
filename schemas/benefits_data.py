from pydantic import BaseModel


class BenefitsDataSh(BaseModel):
    """
    Модель тела запроса о льготах студента.
    """
    benefits: str | None = None
    personal_id: int

