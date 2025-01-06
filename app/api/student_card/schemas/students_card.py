from db.database import APIBase
from api.student_card.schemas.benefits_data import BenefitsDataSh
from api.student_card.schemas.contact_data import ContactDataSh
from api.student_card.schemas.educational_data import EducationalDataSh
from api.student_card.schemas.millitary_data import MilitaryDataSh
from api.student_card.schemas.other_data import OtherDataSh
from api.student_card.schemas.personal_data import PersonalDataSh
from api.student_card.schemas.stipend_data import StipendDataSh
from api.student_card.schemas.history_data import HistoryDataSh
from api.student_card.schemas.order_data import OrderDataSh


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


