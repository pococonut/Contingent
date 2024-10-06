from io import BytesIO
import re

from fastapi import HTTPException
import pandas as pd
import numpy as np


async def read_excel_file(file, begin_row=1):
    """
    Функция для чтения данных excel файла в pandas-объект
    :param begin_row: Строка начала чтения файла
    :param file: Excel-файла
    :return: pandas-объект
    """
    excel_data = BytesIO(file)
    df = pd.read_excel(excel_data, header=begin_row)
    return df


def check_param_existence(params):
    for name, value in params.items():
        if value is None:
            exception_text = f"ID: {params.get('id')}. The requirement parameter '{name}' is empty."
            raise HTTPException(status_code=400, detail=exception_text)


def validate_string_params(params, for_check):
    for name, value in params.items():
        if name not in for_check:
            continue

        if not value.isalpha():
            exception_text = f"ID: {params.get('id')}. The string parameter '{name}' contain wrong symbols."
            raise HTTPException(status_code=400, detail=exception_text)


def validate_personal_data(personal_data):
    not_necessary = ["patronymic"]
    only_str = ["firstname", "lastname", "patronymic"]
    requirement_params = dict((k, v) for k, v in personal_data.items() if k not in not_necessary)
    check_param_existence(requirement_params)
    validate_string_params(requirement_params, only_str)


async def parse_df_row(i, df):
    """
    Функция для считывания данных из pandas-объекта в Python-объекты
    :param i: Номер строки
    :param df: pandas-объект
    :return: Список словарей представляющий собой карту студента
    """

    df = df.replace({np.nan: None})

    personal_data = {"id": i,
                     "firstname": df.at[i, 'Имя'],
                     "lastname": df.at[i, 'Фамилия'],
                     "patronymic": df.at[i, 'Отчество'],
                     "birth_date": df.at[i, 'Дата рожд.'],
                     "birth_place": df.at[i, 'Место рожд.'],
                     "citizenship": df.at[i, 'Гражданство'],
                     "type_of_identity": df.at[i, 'Удостов. личности'],
                     "address": df.at[i, 'Адрес'],
                     "snils": str(df.at[i, 'Снилс']),
                     "study_status": df.at[i, 'Статус внутри вуза'],
                     "general_status": df.at[i, 'Статус общий'],
                     "gender": df.at[i, 'Пол']}

    validate_personal_data(personal_data)

    educational_data = {"faculty": df.at[i, 'Факультет'],
                        "direction": df.at[i, 'Направление'],
                        "course": str(df.at[i, 'Курс']),
                        "department": str(df.at[i, 'Кафедра']),
                        "group": str(df.at[i, 'Группа']),
                        "subgroup": df.at[i, 'Подгруппа'],
                        "book_num": str(df.at[i, 'Номер зачётки']),
                        "form": str(df.at[i, 'Форма обуч.']),
                        "degree": df.at[i, 'Степень обуч.'],
                        "degree_payment": df.at[i, 'Форма обуч. $'],
                        "study_duration": str(df.at[i, 'Период обуч.']),
                        "study_duration_total": str(df.at[i, 'Срок обуч.']),
                        "study_profile": str(df.at[i, 'Профиль обуч.']),
                        "current_year": str(df.at[i, 'Текущий год обуч.']),
                        "personal_id": i, }

    contact_data = {"number": str(df.at[i, 'Тел.']),
                    "spare_number": str(df.at[i, '2й Тел.']),
                    "mail": str(df.at[i, 'Почта']),
                    "personal_id": i}

    benefit_data = {"benefits": str(df.at[i, 'Льготы']),
                    "personal_id": i}

    stipend_data = {"form": str(df.at[i, 'Форма']),
                    "amount": str(df.at[i, 'Сумма']),
                    "personal_id": i, }

    military_data = {"status": str(df.at[i, 'Статус']),
                     "category": str(df.at[i, 'Категория']),
                     "delay": str(df.at[i, 'Отсрочка']),
                     "document": str(df.at[i, 'Документ']),
                     "personal_id": i, }

    other_data = {"parents": str(df.at[i, 'Родители']),
                  "parents_contacts": str(df.at[i, 'Контакты родственников']),
                  "relatives_works": str(df.at[i, 'Места работы родственников']),
                  "relatives_addresses": str(df.at[i, 'Адреса родственников']),
                  "personal_id": i, }

    history_data = {"movements": str(df.at[i, 'История перемещений (курс)']),
                    "statuses": str(df.at[i, 'История статусов']),
                    "personal_id": i, }

    order_data = {"order": str(df.at[i, 'Приказы']),
                  "personal_id": i, }

    return [personal_data, educational_data, stipend_data, contact_data,
            military_data, benefit_data, other_data, history_data, order_data]


async def get_cards_form_df(df):
    """
    Функция для получения списка карт студентов из pandas-объекта
    :param df: pandas-объект содержащий данные студенческих карт
    :return: Список карт студентов
    """
    amount_rows = int(df.shape[0])
    student_cards = []

    for i in range(amount_rows):
        card = await parse_df_row(i, df)
        student_cards.append(card)

    return student_cards
