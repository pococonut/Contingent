from db.database import APIBase
from api.student_card.schemas.benefits import BenefitsDataSh
from api.student_card.schemas.contact import ContactDataSh
from api.student_card.schemas.study import StudyDataSh
from api.student_card.schemas.education import EducationDataSh
from api.student_card.schemas.millitary import MilitaryDataSh
from api.student_card.schemas.reference import ReferenceDataSh
from api.student_card.schemas.personal import PersonalDataShIn


class StudentsCardSh(APIBase):
    """
    Модель тела запроса карты студента.
    """
    personal_data: PersonalDataShIn | None = None
    study_data: StudyDataSh | None = None
    education_data: EducationDataSh | None = None
    benefits_data: BenefitsDataSh | None = None
    contact_data: ContactDataSh | None = None
    military_data: MilitaryDataSh | None = None
    reference_data: ReferenceDataSh | None = None

