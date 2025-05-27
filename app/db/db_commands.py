import logging

from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, delete, update, exc

from db.database import engine, SessionLocal, Base

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
    try:
        if type(data) == dict:
            new_data = table(**data)
        else:
            new_data = table(**data.dict())

        db.add(new_data)
        await db.commit()
        await db.refresh(new_data)
        return data

    except exc.IntegrityError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"IntegrityError: AlreadyExists")
    except exc.DataError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"DataError: {e}")
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def get_table_data_paginate(db, table, item_id=None):
    """
    Функция для получения списка объектов с пагинацией из переданной таблицы БД,
    если item_id=None, иначе функция возвращает данные конкретного объекта
    :param item_id: Уникальный идентификатор объекта
    :param db: Объект сессии
    :param table: Таблица БД
    :return: Данные таблицы
    """
    try:
        stmt = select(table) if item_id is None else select(table).where(table.id == item_id)
        result = await paginate(db, stmt)
        return result
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def get_table_data(db, table, item_id=None):
    """
    Функция для получения списка объектов из переданной таблицы БД,
    если item_id=None, иначе функция возвращает данные конкретного объекта
    :param item_id: Уникальный идентификатор объекта
    :param db: Объект сессии
    :param table: Таблица БД
    :return: Данные таблицы
    """
    try:
        stmt = select(table) if item_id is None else select(table).where(table.id == item_id)
        result = await db.execute(stmt)
        return result.scalars().all()
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def change_data(db, data):
    """
    Функция для изменения параметров переданного объекта
    :param db: Объект сессии
    :param data: Словарь, содержащий имя таблицы,
     параметры для изменения, идентификатор объекта
    :return: Измененный объект
    """
    obj_id = data.get("id")
    table = data.get("table")
    parameters = data.get("parameters")
    obj_id_db = table.id

    try:
        for parameter, new_val in parameters.items():
            stmt = update(table).where(obj_id_db == obj_id)
            stmt = stmt.values({f"{parameter}": new_val})
            await db.execute(stmt)
        await db.commit()

        stmt = select(table).where(obj_id_db == obj_id)
        result = await db.execute(stmt)
        updated_data = result.scalars().all()
        return updated_data
    except exc.IntegrityError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"IntegrityError: AlreadyExists")
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Deletion Error.\n {e}")
