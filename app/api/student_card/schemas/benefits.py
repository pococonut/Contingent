from db.database import APIBase


class BenefitsDataSh(APIBase):
    """
    Модель тела запроса льгот студента.
    """
    benefits_type: str | None = None
    personal_id: int

