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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "personal_data": {
                        "first_name": "Полина",
                        "last_name": "Золотухина",
                        "middle_name": "Викторовна",
                        "birth": "16.09.2003",
                        "place_of_birth": "Тында, Амурская область",
                        "citizenship": "Россия",
                        "identity_cards": "3241552",
                        "residential_address": "Краснодар",
                        "registration_address": "Краснодар",
                        "snils": "1010-12122",
                        "global_status": "студент",
                        "inner_status": "студент",
                        "gender": "ж"
                    },
                    "study_data": {
                        "faculty": "Математика и Компьютерные науки",
                        "direction": "Математика и Компьютерные науки",
                        "course": "4",
                        "group": "42",
                        "subgroup": "42/1",
                        "educational_form": "очно",
                        "degree_of_study": "бакалавр",
                        "learning_conditions": "",
                        "department": "ВМИ",
                        "profile": "Математика",
                        "record_book_number": "123321",
                        "start_date": "01.09.2021",
                        "end_date": "30.08.2025",
                        "period_of_study": "4",
                        "stipend_academic": "нет",
                        "stipend_social": "нет"
                    },
                    "education_data": {
                        "educational_document": "очно",
                        "document_serial_number": "323245"
                    },
                    "benefits_data": {
                        "benefits_type": "льготы"
                    },
                    "contact_data": {
                        "first_phone": "88005353535",
                        "second_phone": "89005055500",
                        "email": "polina@mail.ru"
                    },
                    "military_data": {
                        "status": "нет",
                        "category": "нет",
                        "deferment_end_date": "нет",
                        "document": "нет"
                    },
                    "reference_data": {
                        "first_parent": "Елена В.У.",
                        "second_parent": "Виктор М.М."
                    }
                }
            ]
        }
    }
