import logging
from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy import select, and_, exc

from helpers.dicts import student_card_models_dict
from api.student_card.models.personal import PersonalData
from api.student_card.models.study import StudyData


async def filters_check(db, filters_data):
    """
    Функция для формирования множества идентификаторов студентов,
    подходящих под фильтры
    :param db: Объект сессии
    :param filters_data: Данные для фильтрации: [тип фильтрации, фильтры, таблица]
    :return: Список идентификаторов студентов
    """
    data_type, filters, table = filters_data
    stmt = select(table.personal_id) if data_type != "personal" else select(table.id)
    conditions = []

    for param, value in filters.items():
        if not value:
            continue
        conditions.append(value == getattr(table, param))

    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await db.execute(stmt)
    students_ids = result.scalars().all()

    return students_ids


async def get_suitable_students_ids(db, filters):
    """
    Функция для формирования списка идентификаторов студентов, подходящих под фильтры
    :param db: Объект сессии
    :param filters: Фильтры
    :return: Список подходящих под фильтры студентов
    """
    personal_filter_data = ["personal", filters.get("personal_filters"), PersonalData]
    educational_filter_data = ["educational", filters.get("educational_filters"), StudyData]

    suitable_students_personal = await filters_check(db, personal_filter_data)
    suitable_students_educational = await filters_check(db, educational_filter_data)
    suitable_students = set(suitable_students_educational) & set(suitable_students_personal)

    return suitable_students


async def get_filtered_cards(db, filters: dict = None):
    """
    Функция для получения списка карт студентов
    :param db: Объект сессии
    :param filters: Фильтры
    :return: Словарь карт студентов
    """
    try:
        suitable_students = defaultdict(dict)
        suitable_students_ids = await get_suitable_students_ids(db, filters)

        for student_id in suitable_students_ids:
            for name, table in student_card_models_dict.items():
                param_id = "id" if name == "personal_data" else 'personal_id'
                stmt = select(table).where(student_id == getattr(table, param_id))
                result = await db.execute(stmt)
                data = result.scalars().all()[0]
                suitable_students[student_id][name] = data

        return suitable_students
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")

