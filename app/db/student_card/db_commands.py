import logging
from collections import defaultdict

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, exc

from api.student_card.models import PersonalData
from api.student_card.schemas import StudentsCardSh
from helpers.dicts import student_card_models_dict, student_card_schemas_dict


async def format_card_to_dict(s_card):
    """
    Функция для приведения данных карты студента к нужному виду
    :param s_card: Карта студента типа StudentsCardSh
    :return: Данные карты студента в виде списка словарей
    """
    return {"personal_data": s_card.personal_data.dict(),
            "study_data": s_card.study_data.dict(),
            "education_data": s_card.education_data.dict(),
            "contact_data": s_card.contact_data.dict(),
            "military_data": s_card.military_data.dict(),
            "benefits_data": s_card.benefits_data.dict(),
            "reference_data": s_card.reference_data.dict()}


async def get_cards(db):
    """
    Функция для получения списка карт студентов
    :return: Словарь карт студентов
    """

    suitable_students = defaultdict(dict)
    try:
        stmt = select(PersonalData.id)
        result = await db.execute(stmt)
        suitable_students_ids = result.scalars().all()
        if not suitable_students_ids:
            return {}

        for student_id in suitable_students_ids:
            for name, table in student_card_models_dict.items():
                param_id = "id" if name == "personal_data" else 'personal_id'
                stmt = select(table).where(student_id == getattr(table, param_id))
                result = await db.execute(stmt)
                data = result.scalars().all()[0]
                suitable_students[student_id][name] = student_card_schemas_dict.get(name).from_orm(data)

        return suitable_students
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def get_card(db, student_id):
    """
    Функция для получения списка карт студентов
    :return: Словарь карт студентов
    """

    suitable_students = defaultdict(dict)
    try:
        stmt = select(PersonalData.id).where(PersonalData.id == student_id)
        result = await db.execute(stmt)
        suitable_students_ids = result.scalars().all()

        if not suitable_students_ids:
            return {}

        for student_id in suitable_students_ids:
            for name, table in student_card_models_dict.items():
                param_id = "id" if name == "personal_data" else 'personal_id'
                stmt = select(table).where(student_id == getattr(table, param_id))
                result = await db.execute(stmt)
                data = result.scalars().all()[0]
                suitable_students[student_id][name] = student_card_schemas_dict.get(name).from_orm(data)

        return suitable_students
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def add_student_data(db, student_card):
    """
    Функция для добавления личной карты студента в таблицы БД
    :param db: Объект сессии
    :param student_card: Личная карта
    :return: Объект сессии
    """
    try:
        personal_data = PersonalData(**student_card.get("personal_data"))
        db.add(personal_data)
        await db.commit()
        await db.refresh(personal_data)

        for table_name, table in student_card_models_dict.items():
            if table_name == "personal_data":
                continue
            student_card[table_name].update({"personal_id": personal_data.id})
            db.add(table(**student_card[table_name]))
        return db
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Import Error.\n {e}")


async def add_commit_students_cards(db, student_cards):
    """
    Функция для вставки личных карт студента в таблицы БД
    :param db: Объект сессии
    :param student_cards: Список личных карт
    :return: Список личных карт при успешном выполнении
    """
    try:
        for student_card in student_cards:
            db = await add_student_data(db, student_card)
        await db.commit()
        return student_cards
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Import Error.\n {e}")


async def add_commit_students_card(db, student_card):
    """
    Функция для вставки личной карты студента в таблицы БД
    :param db: Объект сессии
    :param student_card: Личная карта
    :return: Личная карта студента при успешном выполнении
    """
    try:
        db = await add_student_data(db, student_card)
        await db.commit()
        return student_card
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Import Error.\n {e}")


async def change_card(db, data):
    """
    Функция для изменения данных личной карточки студента
    :param db: Объект сессии
    :param data: Словарь, содержащий имя таблицы,
     параметры для изменения, идентификатор студента
    :return: Измененная карточка студента
    """
    table_name = data.get("table_name")
    parameters = data.get("parameters")
    personal_id = data.get("personal_id")

    table = student_card_models_dict.get(table_name)
    student_id = table.id if table_name == "personal_data" else table.personal_id

    try:
        for parameter, new_val in parameters.items():
            stmt = update(table).where(student_id == personal_id)
            stmt = stmt.values({f"{parameter}": new_val})
            await db.execute(stmt)
        await db.commit()

        stmt = select(table).where(student_id == personal_id)
        result = await db.execute(stmt)
        updated_data = result.scalars().all()
        return updated_data

    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")

