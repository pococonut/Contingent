from api.student_card.models.education import EducationData
from api.student_card.schemas.benefits import BenefitsDataSh
from api.student_card.schemas.contact import ContactDataSh
from api.student_card.schemas.education import EducationDataSh
from api.student_card.schemas.millitary import MilitaryDataSh
from api.student_card.schemas.reference import ReferenceDataSh
from api.student_card.schemas.personal import PersonalDataShOut
from api.student_card.models.study import StudyData
from api.student_card.models.personal import PersonalData
from api.student_card.models.contact import ContactData
from api.student_card.models.reference import ReferenceData
from api.student_card.models.benefits import BenefitsData
from api.student_card.models.military import MilitaryData
from api.structure.direction.models import DirectionData
from api.structure.department.models import DepartmentData
from api.structure.group.models import GroupData
from api.structure.profile.models import ProfileData
from api.structure.subgroup.models import SubgroupData
from api.student_card.schemas.study import StudyDataSh
from validation.student_card_parameters import *

student_card_validation_dict = {"personal_data": validate_personal_data,
                                "study_data": validate_study_data,
                                "contact_data": validate_contact_data}

student_params_validation_dict = {"birth": validate_date,
                                  "snils": validate_snils,
                                  "first_phone": validate_phone_number,
                                  "second_phone": validate_phone_number,
                                  "email": validate_mail,
                                  "faculty": validate_education_forms,
                                  "direction": validate_education_forms,
                                  "department": validate_education_forms,
                                  "educational_form": validate_education_forms,
                                  "degree_of_study": validate_education_forms,
                                  "learning_conditions": validate_education_forms,
                                  "course": validate_course,
                                  "group": validate_group,
                                  "subgroup": validate_subgroup,
                                  "record_book_number": validate_student_book}

student_card_models_dict = {"personal_data": PersonalData,
                            "education_data": EducationData,
                            "study_data": StudyData,
                            "contact_data": ContactData,
                            "military_data": MilitaryData,
                            "benefits_data": BenefitsData,
                            "reference_data": ReferenceData}

student_card_schemas_dict = {"personal_data": PersonalDataShOut,
                             "education_data": EducationDataSh,
                             "study_data": StudyDataSh,
                             "contact_data": ContactDataSh,
                             "military_data": MilitaryDataSh,
                             "benefits_data": BenefitsDataSh,
                             "reference_data": ReferenceDataSh}

structure_models_dict = {"department": DepartmentData,
                         "direction": DirectionData,
                         "group": GroupData,
                         "profile": ProfileData,
                         "subgroup": SubgroupData, }

all_models_dict = {**student_card_models_dict, **structure_models_dict}


