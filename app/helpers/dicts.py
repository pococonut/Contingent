from api.student_card.schemas.benefits import BenefitsDataSh
from api.student_card.schemas.contact import ContactDataSh
from api.student_card.schemas.millitary import MilitaryDataSh
from api.student_card.schemas.other import OtherDataSh
from api.student_card.schemas.personal import PersonalDataSh
from api.student_card.schemas.stipend import StipendDataSh
from api.student_card.models.study import StudyData
from api.student_card.models.personal import PersonalData
from api.student_card.models.contact import ContactData
from api.student_card.models.other import OtherData
from api.student_card.models.stipend import StipendData
from api.student_card.models.benefits import BenefitsData
from api.student_card.models.military import MilitaryData
from api.structure.direction.models import DirectionData
from api.structure.department.models import DepartmentData
from api.structure.group.models import GroupData
from api.structure.profile.models import ProfileData
from api.structure.subgroup.models import SubgroupData
from validation.student_card_parameters import *

student_card_validation_dict = {"personal_data": validate_personal_data,
                                "study_data": validate_study_data,
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
                            "study_data": StudyData,
                            "stipend_data": StipendData,
                            "contact_data": ContactData,
                            "military_data": MilitaryData,
                            "benefits_data": BenefitsData,
                            "other_data": OtherData}

structure_models_dict = {"department": DepartmentData,
                         "direction": DirectionData,
                         "group": GroupData,
                         "profile": ProfileData,
                         "subgroup": SubgroupData, }

all_models_dict = {**student_card_models_dict, **structure_models_dict}

schemas_dict = {"personal_data": PersonalDataSh,
                "study_data": StudyData,
                "stipend_data": StipendDataSh,
                "contact_data": ContactDataSh,
                "military_data": MilitaryDataSh,
                "benefits_data": BenefitsDataSh,
                "other_data": OtherDataSh}
