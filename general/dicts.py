from schemas.benefits_data import BenefitsDataSh
from schemas.contact_data import ContactDataSh
from schemas.educational_data import EducationalDataSh
from schemas.millitary_data import MilitaryDataSh
from schemas.other_data import OtherDataSh
from schemas.personal_data import PersonalDataSh
from schemas.stipend_data import StipendDataSh
from schemas.history_data import HistoryDataSh
from schemas.order_data import OrderDataSh
from models.educational_data import EducationalData
from models.personal_data import PersonalData
from models.contact_data import ContactData
from models.other_data import OtherData
from models.stipend_data import StipendData
from models.benefits_data import BenefitsData
from models.military_data import MilitaryData
from models.history_data import HistoryData
from models.order_data import OrderData


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
