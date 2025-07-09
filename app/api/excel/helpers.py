from io import BytesIO

import pandas as pd
import numpy as np

from validation.student_card_parameters import validate_personal_data, validate_study_data, validate_contact_data


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


async def parse_df_row(i, df):
    """
    Функция для считывания данных из pandas-объекта в Python-объекты
    :param i: Номер строки
    :param df: pandas-объект
    :return: Список словарей представляющий собой карту студента
    """

    df = df.replace({np.nan: ""})

    personal_data = {"id": i,
                     "first_name": df.at[i, 'Имя'],
                     "last_name": df.at[i, 'Фамилия'],
                     "middle_name": df.at[i, 'Отчество'],
                     "birth": str(df.at[i, 'Дата рожд.']),
                     "place_of_birth": df.at[i, 'Место рожд.'],
                     "citizenship": df.at[i, 'Гражданство'],
                     "identity_cards": df.at[i, 'Удостов. личности'],
                     "residential_address": df.at[i, 'Адрес проживания'],
                     "registration_address": df.at[i, 'Адрес регистрации'],
                     "snils": str(df.at[i, 'Снилс']),
                     "inner_status": df.at[i, 'Статус внутри вуза'],
                     "global_status": df.at[i, 'Статус общий'],
                     "gender": df.at[i, 'Пол']}

    validate_personal_data(personal_data)

    educational_data = {"educational_document": str(df.at[i, 'Документ об образовании']),
                        "document_serial_number": str(df.at[i, 'Серийный номер документа'])}

    study_data = {"faculty": df.at[i, 'Факультет'],
                  "course": str(df.at[i, 'Курс']),
                  "direction": df.at[i, 'Направление'],
                  "group": str(df.at[i, 'Группа']),
                  "subgroup": df.at[i, 'Подгруппа'],
                  "educational_form": str(df.at[i, 'Форма обуч.']),
                  "degree_of_study": df.at[i, 'Степень обуч.'],
                  "learning_conditions": df.at[i, 'Форма обуч. $'],
                  "department": str(df.at[i, 'Кафедра']),
                  "profile": str(df.at[i, 'Профиль обуч.']),
                  "record_book_number": str(df.at[i, 'Номер зачётки']),
                  "start_date": str(df.at[i, 'Начало обучения']),
                  "end_date": str(df.at[i, 'Конец обучения']),
                  "period_of_study": str(df.at[i, 'Период обуч.']),
                  "stipend_academic": str(df.at[i, 'Академическая стипендия']),
                  "stipend_social": str(df.at[i, 'Социальная стипендия']),
                  "personal_id": i, }

    validate_study_data(study_data)

    contact_data = {"first_phone": str(df.at[i, 'Тел.']),
                    "second_phone": str(df.at[i, '2й Тел.']),
                    "email": str(df.at[i, 'Почта']),
                    "personal_id": i}

    validate_contact_data(contact_data)

    benefits_data = {"benefits_type": str(df.at[i, 'Тип льгот']),
                     "personal_id": i}

    military_data = {"status": str(df.at[i, 'Статус']),
                     "category": str(df.at[i, 'Категория']),
                     "deferment_end_date": str(df.at[i, 'Отсрочка']),
                     "document": str(df.at[i, 'Документ']),
                     "personal_id": i, }

    reference_data = {"first_parent": str(df.at[i, 'Родитель 1']),
                      "second_parent": str(df.at[i, 'Родитель 2']),
                      "personal_id": i, }

    return {"personal_data": personal_data,
            "study_data": study_data,
            "education_data": educational_data,
            "contact_data": contact_data,
            "military_data": military_data,
            "benefits_data": benefits_data,
            "reference_data": reference_data}


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

    print(student_cards)
    return student_cards
