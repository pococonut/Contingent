from db.database import APIBase


class EducationalDataSh(APIBase):
    """
    Модель тела запроса учебной деятельности студента.
    """
    faculty: str | None = None
    direction: str | None = None
    course: str | None = None
    department: str | None = None
    group: str | None = None
    subgroup: str | None = None
    form: str | None = None
    book_num: str | None = None
    degree: str | None = None
    degree_payment: str | None = None
    study_duration: str | None = None
    study_duration_total: str | None = None
    study_profile: str | None = None
    current_year: str | None = None

    personal_id: int | None = None

