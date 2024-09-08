import asyncio
import logging
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy import select, update, delete

from db.database import engine, SessionLocal, Base
from general.dicts import schemas_dict, models_dict
from models.personal_data import PersonalData
from schemas.educational_data import EducationalDataSh
from schemas.personal_data import PersonalDataSh
from models.educational_data import EducationalData
from schemas.students_card import StudentsCardSh

logging.basicConfig(filename='db_log.log', level=logging.INFO,
                    filemode="w", format="%(asctime)s %(levelname)s %(message)s")


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
    async with db.begin():
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
    return [s_card.personal_data.dict(),
            s_card.educational_data.dict(),
            s_card.stipend_data.dict(),
            s_card.contact_data.dict(),
            s_card.military_data.dict(),
            s_card.benefits_data.dict(),
            s_card.other_data.dict(),
            s_card.history_data.dict(),
            s_card.order_data.dict()]


async def add_student_data(db, student_card):
    """
    Функция для добавления личных карт студента в таблицы БД
    :param db: Объект сессии
    :param student_card: Личная карта
    :return: Объект сессии
    """
    models = models_dict.values()
    for data, table in zip(student_card, models):
        db.add(table(**data))
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


async def personal_filters_check(students_cards, p_filters):
    """
    Функция для формирования множества идентификаторов студентов,
    подходящих под фильтры персональной информации
    :param students_cards: Список карт всех студентов
    :param p_filters: Фильтры персональной информации
    :return: Множество идентификаторов студентов
    """
    firstname, lastname = p_filters
    suitable_students = set()
    for p_data in students_cards.get("personal_data"):
        p_data = PersonalDataSh.from_orm(p_data).dict()

        if firstname and p_data.get("firstname") != firstname:
            continue
        if lastname and p_data.get("lastname") != lastname:
            continue
        suitable_students.add(p_data.get("id"))

    return suitable_students


async def educational_filters_check(students_cards, ed_filters):
    """
    Функция для формирования множества идентификаторов студентов,
    подходящих под фильтры учебной информации
    :param students_cards: Список карт всех студентов
    :param ed_filters: Фильтры учебной информации
    :return: Множество идентификаторов студентов
    """
    faculty, direction, course, department, group, subgroup = ed_filters
    suitable_students = set()
    for ed_data in students_cards.get("educational_data"):
        ed_data = EducationalDataSh.from_orm(ed_data).dict()

        if faculty and ed_data.get("faculty") != faculty:
            continue
        if direction and ed_data.get("direction") != direction:
            continue
        if course and ed_data.get("course") != course:
            continue
        if department and ed_data.get("department") != department:
            continue
        if group and ed_data.get("group") != group:
            continue
        if subgroup and ed_data.get("subgroup") not in subgroup:
            continue
        suitable_students.add(ed_data.get("personal_id"))

    return suitable_students


async def get_suitable_students_ids(students_cards, filters):
    """
    Функция для формирования списка подходящих под фильтры студентов
    :param students_cards: Список карт всех студентов
    :param filters: Фильтры
    :return: Список подходящих под фильтры студентов
    """
    personal_filters = filters.get("personal_filters")
    educational_filters = filters.get("educational_filters")

    suitable_students_personal = await personal_filters_check(students_cards, personal_filters)
    suitable_students_educational = await educational_filters_check(students_cards, educational_filters)
    suitable_students = suitable_students_educational & suitable_students_personal

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
        students_cards = await get_tables_data(db)
        suitable_students_ids = await get_suitable_students_ids(students_cards, filters)

        for table_name, rows in students_cards.items():
            for row in rows:
                schema = schemas_dict.get(table_name)
                data = schema.from_orm(row).dict()

                if table_name == "personal_data":
                    student_id = data.get("id")
                    del data['id']
                else:
                    student_id = data.get("personal_id")
                    del data['personal_id']

                if student_id in suitable_students_ids:
                    suitable_students[student_id].update(data)

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


async def drop_table():
    async with engine.begin() as conn:
        # Удаление таблицы
        await conn.run_sync(EducationalData.metadata.drop_all)


async def main():
    await drop_table()

# asyncio.run(main())
