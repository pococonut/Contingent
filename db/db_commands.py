import asyncio
import logging
from collections import defaultdict

from sqlalchemy import select

from db.database import engine, SessionLocal, Base
from general.dicts import schemas_dict, models_dict
from schemas.educational_data import EducationalDataSh
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
            await db.commit()
            await db.refresh(new_data)
            return data
        except Exception as e:
            logging.error(e)


async def add_students_card(db, student_card):
    """
    Функция для вставки личной карты студента в таблицы БД
    :param db: Объект сессии
    :param student_card: Данные
    :return: Карта студента при успешном выполнении
    """
    try:
        models = models_dict.values()
        if type(student_card) is StudentsCardSh:
            student_card = [student_card.personal_data.dict(),
                            student_card.educational_data.dict(),
                            student_card.stipend_data.dict(),
                            student_card.contact_data.dict(),
                            student_card.military_data.dict(),
                            student_card.benefits_data.dict(),
                            student_card.other_data.dict()]

        for data, table in zip(student_card, models):
            await add_data_to_table(db, data, table)
        return student_card

    except Exception as e:
        logging.error(e)


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


async def get_filtered_cards(db, filters: dict = None):
    """
    Функция для получения списка карт студентов
    :param db: Объект сессии
    :param filters: Фильтры
    :return: Словарь карт студентов
    """
    try:
        suitable_students_ids = []
        suitable_students = defaultdict(dict)
        students_cards = await get_tables_data(db)
        faculty, direction, course, department, group, subgroup = filters.values()

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
            suitable_students_ids.append(ed_data.get("personal_id"))

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


async def drop_table():
    async with engine.begin() as conn:
        # Удаление таблицы
        await conn.run_sync(EducationalData.metadata.drop_all)


async def main():
    await drop_table()

# asyncio.run(main())
