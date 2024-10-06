from schemas.student_card.benefits_data import BenefitsDataSh
from schemas.student_card.contact_data import ContactDataSh
from schemas.student_card.educational_data import EducationalDataSh
from schemas.student_card.millitary_data import MilitaryDataSh
from schemas.student_card.other_data import OtherDataSh
from schemas.student_card.personal_data import PersonalDataSh
from schemas.student_card.stipend_data import StipendDataSh
from schemas.student_card.history_data import HistoryDataSh
from schemas.student_card.order_data import OrderDataSh
from models.student_card.educational_data import EducationalData
from models.student_card.personal_data import PersonalData
from models.student_card.contact_data import ContactData
from models.student_card.other_data import OtherData
from models.student_card.stipend_data import StipendData
from models.student_card.benefits_data import BenefitsData
from models.student_card.military_data import MilitaryData
from models.student_card.history_data import HistoryData
from models.student_card.order_data import OrderData
from models.user import User


fake_users_db = {
    "po": User(username="po",
               password="$2b$12$5coZhCR2ZV3ZOOP9N9PVQukpOSSJu5HnKWUSrIRsdXhSjTiqp7nqW",
               access_token="access-token",
               refresh_token="refresh-token")
}

models_dict = {"personal_data": PersonalData,
               "educational_data": EducationalData,
               "stipend_data": StipendData,
               "contact_data": ContactData,
               "military_data": MilitaryData,
               "benefits_data": BenefitsData,
               "other_data": OtherData,
               "history_data": HistoryData,
               "order_data": OrderData}


schemas_dict = {"personal_data": PersonalDataSh,
                "educational_data": EducationalDataSh,
                "stipend_data": StipendDataSh,
                "contact_data": ContactDataSh,
                "military_data": MilitaryDataSh,
                "benefits_data": BenefitsDataSh,
                "other_data": OtherDataSh,
                "history_data": HistoryDataSh,
                "order_data": OrderDataSh}
