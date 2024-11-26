import asyncio
import logging

from fastapi import HTTPException
from sqlalchemy import select, delete, exc

from db.database import engine, SessionLocal, Base
from helpers.dicts import student_card_models_dict
from models.student_card.personal_data import PersonalData
from models.student_card.educational_data import EducationalData
from models.structure.subgroup import SubgroupData
from models.structure.direction import DirectionData
from models.structure.group import GroupData
from models.structure.profile import ProfileData
from models.structure.department import DepartmentData
from models.structure.fgos import FgosData
from models.student_list.planned_num_contingent import PlannedNumContingent
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
        await db.commit()
        await db.refresh(new_data)
        return data

    except exc.DataError as e:
        logging.error(e)
    except exc.SQLAlchemyError as e:
        logging.error(e)


async def get_table_data(db, table):
    """
    Функция для получения данных из переданной таблицы БД
    :param db: Объект сессии
    :param table: Таблица БД
    :return: Данные таблицы
    """
    try:
        stmt = select(table)
        result = await db.execute(stmt)
        return result.scalars().all()
    except exc.SQLAlchemyError as e:
        logging.error(e)


async def delete_object(db, obj_id, table_name):
    """
    Функция для удаления объекта из таблицы БД
    :param db: Объект сессии
    :param obj_id: Идентификатор объекта
    :param table_name: Название таблицы
    :return: Идентификатор удаленного объекта при успешном выполнении
    """
    try:
        await db.execute(delete(table_name).where(table_name.id == obj_id))
        await db.commit()
        return {"result": f"Object {obj_id} was successfully deleted"}
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=f"Deletion Error.\n {e}")
