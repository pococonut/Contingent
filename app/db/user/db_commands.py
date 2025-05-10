import logging
import os

import aiofiles
from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, exc, and_, update

from api.user.models.user import User
from db.db_commands import change_data


async def add_user_to_db(db, user):
    """
    Функция для вставки ПользователяИ в талицу БД
    :param db: Объект сессии
    :param user: Данные
    :return: Добавленные данные
    """
    try:
        user_dict = user.dict()

        first_name_0 = f"{user_dict.get('first_name')[0]}."
        middle_name_0 = f"{user_dict.get('middle_name')[0]}." if user_dict.get('middle_name') else ""
        user_dict["short_name"] = f"{user_dict.get('last_name')} {first_name_0}{middle_name_0}"

        user_model = User(**user_dict)
        db.add(user_model)
        await db.commit()
        await db.refresh(user_model)
        return user_model
    except exc.IntegrityError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"IntegrityError: AlreadyExists")
    except exc.DataError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"DataError: {e}")
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def get_users_from_db(db):
    """
    Функция для получения словаря пользователей
    :param db: Объект сессии
    """
    try:
        stmt = select(User)
        result = await db.execute(stmt)
        users = result.scalars().all()
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")

    users_from_db = {}
    for user_db in users:
        users_from_db[user_db.login] = user_db

    return users_from_db


async def get_user_by_name(db, user_name):
    """
    Функция для получения данных пользователя по ФИО
    :param db: Объект сессии
    :param user_name: словарь ФИО пользователя
    """
    try:
        f_name = user_name.get("first_name")
        l_name = user_name.get("last_name")
        m_name = user_name.get("middle_name")
        stmt = select(User).where(and_(User.first_name == f_name,
                                       User.last_name == l_name,
                                       User.middle_name == m_name)
                                  if m_name
                                  else
                                  and_(User.first_name == f_name,
                                       User.last_name == l_name))
        result = await paginate(db, stmt)
        return result
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def add_user_photo(db, user_id, file):
    """
    Функция для добавления фото пользователя
    :param db: Объект сессии
    :param user_id: id пользователя
    :param file: Фото пользователя
    """
    data = await file.read()
    file_path = f"../user_photo/{user_id}"
    file_route = f"/user_photo/{user_id}"
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(data)
    try:
        stmt = update(User).where(User.id == user_id)
        stmt = stmt.values({"photo": file_route})
        await db.execute(stmt)
        await db.commit()
        return {"response": "Success"}
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")


async def delete_user_photo(db, user_id):
    """
    Функция для удаления фото пользователя
    :param db: Объект сессии
    :param user_id: id пользователя
    """
    file_path = f"../user_photo/{user_id}"
    data = {"id": user_id,
            "table": User,
            "parameters": {"photo": None}}
    try:
        os.remove(file_path)
        await change_data(db, data)
        return {"response": "Success"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")
