from db.database import APIBase
from api.student_card.schemas.benefits import BenefitsDataSh
from api.student_card.schemas.contact import ContactDataSh
from api.student_card.schemas.study import StudyDataSh
from api.student_card.schemas.education import EducationDataSh
from api.student_card.schemas.millitary import MilitaryDataSh
from api.student_card.schemas.other import OtherDataSh
from api.student_card.schemas.personal import PersonalDataSh
from api.student_card.schemas.stipend import StipendDataSh


class StudentsCardSh(APIBase):
    """
    Модель тела запроса карты студента.
    """
    personal_data: PersonalDataSh | None = None
    study_data: StudyDataSh | None = None
    education_data: EducationDataSh | None = None
    benefits_data: BenefitsDataSh | None = None
    contact_data: ContactDataSh | None = None
    military_data: MilitaryDataSh | None = None
    stipend_data: StipendDataSh | None = None
    other_data: OtherDataSh | None = None


