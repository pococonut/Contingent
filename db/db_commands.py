import asyncio
import logging

from sqlalchemy import select

from db.database import engine, SessionLocal, Base
from general.dicts import student_card_models_dict
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


async def get_table_data(db, table):
    try:
        stmt = select(table)
        result = await db.execute(stmt)
        return result.scalars().all()
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
        for table_name, table_model in student_card_models_dict.items():
            stmt = select(table_model)
            result = await db.execute(stmt)
            data[table_name] = result.scalars().all()
        return data
    except Exception as e:
        logging.error(e)
