from db.database import APIBase


class EducationDataSh(APIBase):
    """
    Модель тела запроса образования студента.
    """
    educational_document: str | None = None
    document_serial_number: str | None = None

    personal_id: int

