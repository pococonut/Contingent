from db.database import APIBase
from schemas.student_card.benefits_data import BenefitsDataSh
from schemas.student_card.contact_data import ContactDataSh
from schemas.student_card.educational_data import EducationalDataSh
from schemas.student_card.millitary_data import MilitaryDataSh
from schemas.student_card.other_data import OtherDataSh
from schemas.student_card.personal_data import PersonalDataSh
from schemas.student_card.stipend_data import StipendDataSh
from schemas.student_card.history_data import HistoryDataSh
from schemas.student_card.order_data import OrderDataSh


class StudentsCardSh(APIBase):
    """
    Модель тела запроса карты студента.
    """
    personal_data: PersonalDataSh | None = None
    educational_data: EducationalDataSh | None = None
    benefits_data: BenefitsDataSh | None = None
    contact_data: ContactDataSh | None = None
    military_data: MilitaryDataSh | None = None
    stipend_data: StipendDataSh | None = None
    other_data: OtherDataSh | None = None
    history_data: HistoryDataSh | None = None
    order_data: OrderDataSh | None = None


