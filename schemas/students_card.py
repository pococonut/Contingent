from pydantic import BaseModel

from schemas.benefits_data import BenefitsDataSh
from schemas.contact_data import ContactDataSh
from schemas.educational_data import EducationalDataSh
from schemas.millitary_data import MilitaryDataSh
from schemas.other_data import OtherDataSh
from schemas.personal_data import PersonalDataSh
from schemas.stipend_data import StipendDataSh
from schemas.history_data import HistoryDataSh
from schemas.order_data import OrderDataSh


class StudentsCardSh(BaseModel):
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

    class Config:
        orm_mode = True
        from_attributes = True

