import re

from fastapi import HTTPException


def check_param_existence(params):
    """
    Функция проверяет наличие обязательных параметров
    :param params: Данные студенческой карты
    """
    for name, value in params.items():
        if value is None:
            exception_text = f"ID: {params.get('id')}. The requirement parameter '{name}' is empty."
            raise HTTPException(status_code=400, detail=exception_text)


def get_only_requirement(data, not_necessary):
    """
    Функция отбирает только обязательные параметры
    :param data: Данные студенческой карты
    :param not_necessary: Необязательные параметры
    """
    return dict((k, v) for k, v in data.items() if k not in not_necessary)


def check_requirement_params(not_necessary, params):
    """
    Функция проверяет обязательные параметры
    :param not_necessary: Необязательные параметры
    :param params: Данные студенческой карты
    """
    requirement_params = get_only_requirement(params, not_necessary)
    check_param_existence(requirement_params)


def validate_string_params(params, for_check):
    """
    Функция проверяет параметры на соответствие строковому типу
    :param params: Данные студенческой карты
    :param for_check: Проверяемые параметры
    """
    for name, value in params.items():
        if name not in for_check:
            continue

        if value and not value.isalpha():
            exception_text = f"ID: {params.get('id')}. The string parameter '{name}' contain wrong symbols."
            raise HTTPException(status_code=400, detail=exception_text)


def validate_date(params):
    """
    Функция проверяет соответствие дат шаблону
    :param params: Данные студенческой карты
    """
    pattern = r"\d\d\.\d\d\.\d{4}"
    if not re.fullmatch(pattern, params.get("birth_date")):
        exception_text = f"ID: {params.get('id')}. Wrong date format."
        raise HTTPException(status_code=400, detail=exception_text)


def validate_snils(params):
    """
    Функция проверяет соответствие номера снилса шаблону
    :param params: Данные студенческой карты
    """
    pattern = r"\d{3}-\d{3}-\d{3} \d\d"  # 123-456-789 12
    if not re.fullmatch(pattern, params.get("snils")):
        exception_text = f"ID: {params.get('id')}. Wrong snils format."
        raise HTTPException(status_code=400, detail=exception_text)


def validate_personal_data(personal_data):
    """
    Функция валидирует Персональные данные студента
    :param personal_data: Персональные данные студента
    """
    not_necessary = ["middle_name"]
    only_str = ["first_name", "last_name", "middle_name"]
    check_requirement_params(not_necessary, personal_data)
    validate_string_params(personal_data, only_str)
    # validate_date(personal_data)
    # validate_snils(personal_data)


def validate_phone_number(params):
    """
    Функция проверяет форматы номеров телефонов
    :param params: Данные студенческой карты
    """
    phones = []
    for key, value in params.items():
        if "phone" in key and value:
            phones.append(value)

    for phone in phones:
        phone = phone.split(".")[0]
        if len(phone) != 11 or not phone.isdigit():
            exception_text = f"ID: {params.get('personal_id')}. Wrong phone format."
            raise HTTPException(status_code=400, detail=exception_text)


def validate_mail(params):
    """
    Функция проверяет формат почты
    :param params: Данные студенческой карты
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, params.get("mail")):
        exception_text = f"ID: {params.get('personal_id')}. Wrong mail format."
        raise HTTPException(status_code=400, detail=exception_text)


def validate_contact_data(contact_data):
    """
    Функция валидирует Контактные данные студента
    :param contact_data: Контактные данные студента
    """
    not_necessary = ["spare_number"]
    requirement_params = get_only_requirement(contact_data, not_necessary)
    check_param_existence(requirement_params)
    # validate_phone_number(contact_data)
    # validate_mail(contact_data)


def validate_education_forms(params):
    """
    Функция проверяет соответствие названий форматов обучения форматам из справочника
    :param params: Данные студенческой карты
    """
    # "Справочники" - В дальнейшем будут занесены в бд
    faculties = ['фмикн']
    directions = ['микн', 'фмим']
    departments = ['вми']
    forms = ['очно', 'заочно']
    degree = ['бакалавр', 'магистр', 'аспирант']
    degree_payment = ['бюджет', 'договор']

    forms_lists = [faculties, directions, departments, forms, degree, degree_payment]
    forms = ["faculty", "direction", "department", "form", "degree", "degree_payment"]

    for form, list_necessity in zip(forms, forms_lists):
        if params.get(form).lower() not in list_necessity:
            exception_text = f"ID: {params.get('personal_id')}. Wrong {form} name."
            raise HTTPException(status_code=400, detail=exception_text)


def validate_course(params):
    """
    Функция проверяет формат курса
    :param params: Данные студенческой карты
    """
    exception_text = f"ID: {params.get('personal_id')}. Wrong course format."

    if not params.get("course").isdigit():
        raise HTTPException(status_code=400, detail=exception_text)
    if 1 > int(params.get("course")) > 5:
        raise HTTPException(status_code=400, detail=exception_text)


def validate_group(params):
    """
    Функция проверяет формат группы
    :param params: Данные студенческой карты
    """
    if not params.get('group').isdigit():
        exception_text = f"ID: {params.get('personal_id')}. Wrong group format."
        raise HTTPException(status_code=400, detail=exception_text)


def validate_subgroup(params):
    """
    Функция проверяет формат подгруппы
    :param params: Данные студенческой карты
    """
    pattern = r"\d\d/\d"
    if not re.match(pattern, params.get('subgroup')):
        exception_text = f"ID: {params.get('personal_id')}. Wrong subgroup format."
        raise HTTPException(status_code=400, detail=exception_text)


def validate_student_book(params):
    """
    Функция проверяет формат зачетной книжки
    :param params: Данные студенческой карты
    """
    if not params.get("record_book_number").isdigit():
        exception_text = f"ID: {params.get('personal_id')}. Wrong book number format."
        raise HTTPException(status_code=400, detail=exception_text)


def validate_study_data(study_data):
    """
    Функция проверяет Учебные данные студента
    :param study_data: Учебные данные студента
    """
    not_necessary = []
    check_requirement_params(not_necessary, study_data)
    # validate_education_forms(study_data)
    validate_course(study_data)
    # validate_group(study_data)
    # validate_subgroup(study_data)
    validate_student_book(study_data)


def validate_other_data(other_data):
    """
    Функция проверяет Справочные данные студента
    :param other_data: Справочные данные студента
    """
    not_necessary = []
    check_requirement_params(not_necessary, other_data)
