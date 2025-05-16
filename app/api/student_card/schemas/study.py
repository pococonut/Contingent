from db.database import APIBase


class StudyDataSh(APIBase):
    """
    Модель тела запроса учебной деятельности студента.
    """
    faculty: str
    direction: str
    course: str
    group: str
    subgroup: str
    educational_form: str
    degree_of_study: str
    learning_conditions: str
    department: str | None = None
    profile: str | None = None
    record_book_number: str
    start_date: str
    end_date: str
    period_of_study: str | None = None
    stipend_academic: str | None = None
    stipend_social: str | None = None

    personal_id: int

