import asyncio
import logging
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy import select, update, and_

from db.database import engine, SessionLocal, Base
from general.dicts import models_dict

from models.student_card.personal_data import PersonalData
from models.student_card.educational_data import EducationalData
from models.structure.subgroup import SubgroupData
from models.structure.direction import DirectionData
from models.structure.group import GroupData
from models.structure.profile import ProfileData
from models.structure.department import DepartmentData
from models.auth.user import User

logging.basicConfig(filename='db_log.log', level=logging.INFO,
                    filemode="w", format="%(asctime)s %(levelname)s %(message)s")


async def drop_table():
    async with engine.begin() as conn:
        # Удаление таблицы
        await conn.run_sync(EducationalData.metadata.drop_all)


async def main():
    await drop_table()

# asyncio.run(main())


async def get_db():
    """
    Функция инициализирует базу данных при первом
    вызове и создает новую сессию базы данных
    :return: Объект сессии
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def add_data_to_table(db, data, table):
    """
    Функция для вставки данных в талицу БД
    :param db: Объект сессии
    :param data: Данные
    :param table: Таблица
    :return: Добавленные данные
    """
    try:
        if type(data) == dict:
            new_data = table(**data)
        else:
            new_data = table(**data.dict())

        db.add(new_data)
    except Exception as e:
        logging.error(e)

    await db.commit()
    await db.refresh(new_data)
    return data


async def format_card_to_dict(s_card):
    """
    Функция для приведения данных карты студента к нужному виду
    :param s_card: Карта студента типа StudentsCardSh
    :return: Данные карты студента в виде списка словарей
    """
    return {"personal_data": s_card.personal_data.dict(),
            "educational_data": s_card.educational_data.dict(),
            "stipend_data": s_card.stipend_data.dict(),
            "contact_data": s_card.contact_data.dict(),
            "military_data": s_card.military_data.dict(),
            "benefits_data": s_card.benefits_data.dict(),
            "other_data": s_card.other_data.dict(),
            "history_data": s_card.history_data.dict(),
            "order_data": s_card.order_data.dict()}


async def add_student_data(db, student_card):
    """
    Функция для добавления личной карты студента в таблицы БД
    :param db: Объект сессии
    :param student_card: Личная карта
    :return: Объект сессии
    """
    for table_name, table in models_dict.items():
        db.add(table(**student_card.get(table_name)))
    return db


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
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=f"Import Error.\n {e}")

    return student_cards


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
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=f"Import Error.\n {e}")

    return student_card


async def get_tables_data(db):
    """
    Функция для получения всех карт студентов
    :param db: Объект сессии
    :return: Все карты студентов
    """
    data = {}
    try:
        for table_name, table_model in models_dict.items():
            stmt = select(table_model)
            result = await db.execute(stmt)
            data[table_name] = result.scalars().all()
        return data

    except Exception as e:
        logging.error(e)


async def filters_check(db, filters_data):
    """
    Функция для формирования множества идентификаторов студентов,
    подходящих под фильтры
    :param db: Объект сессии
    :param filters_data: Данные для фильтрации: [тип фильтрации, фильтры, таблица]
    :return: Список идентификаторов студентов
    """
    data_type, filters, table = filters_data
    if data_type != "personal":
        stmt = select(table.personal_id)
    else:
        stmt = select(table.id)

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
    Функция для формирования списка идентификаторов студентов подходящих под фильтры
    :param db: Объект сессии
    :param filters: Фильтры
    :return: Список подходящих под фильтры студентов
    """
    personal_filter_data = ["personal", filters.get("personal_filters"), PersonalData]
    educational_filter_data = ["educational", filters.get("educational_filters"), EducationalData]

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
            for name, table in models_dict.items():
                if name == "personal_data":
                    param_id = "id"
                else:
                    param_id = 'personal_id'
                stmt = select(table).where(student_id == getattr(table, param_id))
                result = await db.execute(stmt)
                data = result.scalars().all()[0]
                suitable_students[student_id][name] = data

        return suitable_students
    except Exception as e:
        logging.error(e)


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

    table = models_dict.get(table_name)

    if table_name == "personal_data":
        student_id = table.id
    else:
        student_id = table.personal_id

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

    except Exception as e:
        logging.error(e)


async def delete_card(db, p_id):
    """
    Функция для удаления личной карточки студента
    :param db: Объект сессии
    :param p_id: Идентификатор студента
    :return: Идентификатор студента при успешном выполнении
    """
    try:
        student = await db.get(PersonalData, p_id)
        await db.delete(student)
        await db.commit()
        return {"result": f"Student {p_id} was successfully deleted"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=f"Deletion Error.\n {e}")

