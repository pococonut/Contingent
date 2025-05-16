from api.student_card.schemas.benefits import BenefitsDataSh
from api.student_card.schemas.contact import ContactDataSh
from api.student_card.schemas.study import EducationalDataSh
from api.student_card.schemas.millitary import MilitaryDataSh
from api.student_card.schemas.other import OtherDataSh
from api.student_card.schemas.personal import PersonalDataSh
from api.student_card.schemas.stipend import StipendDataSh
from api.student_card.schemas.history import HistoryDataSh
from api.student_card.schemas.order import OrderDataSh
from api.student_card.models.study import EducationalData
from api.student_card.models.personal import PersonalData
from api.student_card.models.contact import ContactData
from api.student_card.models.other import OtherData
from api.student_card.models.stipend import StipendData
from api.student_card.models.benefits import BenefitsData
from api.student_card.models.military import MilitaryData
from api.student_card.models.history import HistoryData
from api.student_card.models.order import OrderData
from api.structure.direction.models import DirectionData
from api.structure.department.models import DepartmentData
from api.structure.group.models import GroupData
from api.structure.profile.models import ProfileData
from api.structure.subgroup.models import SubgroupData
from validation.student_card_parameters import *

student_card_validation_dict = {"personal_data": validate_personal_data,
                                "educational_data": validate_educational_data,
                                "contact_data": validate_contact_data,
                                "other_data": validate_other_data, }

student_params_validation_dict = {"birth_date": validate_date,
                                  "snils": validate_snils,
                                  "number": validate_phone_number,
                                  "spare_number": validate_phone_number,
                                  "mail": validate_mail,
                                  "faculty": validate_education_forms,
                                  "direction": validate_education_forms,
                                  "department": validate_education_forms,
                                  "form": validate_education_forms,
                                  "degree": validate_education_forms,
                                  "degree_payment": validate_education_forms,
                                  "course": validate_course,
                                  "group": validate_group,
                                  "subgroup": validate_subgroup,
                                  "book_num": validate_student_book}

student_card_models_dict = {"personal_data": PersonalData,
                            "educational_data": EducationalData,
                            "stipend_data": StipendData,
                            "contact_data": ContactData,
                            "military_data": MilitaryData,
                            "benefits_data": BenefitsData,
                            "other_data": OtherData,
                            "history_data": HistoryData,
                            "order_data": OrderData}

structure_models_dict = {"department": DepartmentData,
                         "direction": DirectionData,
                         "group": GroupData,
                         "profile": ProfileData,
                         "subgroup": SubgroupData, }

all_models_dict = {**student_card_models_dict, **structure_models_dict}

schemas_dict = {"personal_data": PersonalDataSh,
                "educational_data": EducationalDataSh,
                "stipend_data": StipendDataSh,
                "contact_data": ContactDataSh,
                "military_data": MilitaryDataSh,
                "benefits_data": BenefitsDataSh,
                "other_data": OtherDataSh,
                "history_data": HistoryDataSh,
                "order_data": OrderDataSh}
