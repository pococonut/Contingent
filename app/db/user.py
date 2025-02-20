import logging

from fastapi import HTTPException, status
from sqlalchemy import select, delete, exc, and_

from api.user.models import User
from db.db_commands import get_table_data
from db.database import engine, SessionLocal, Base
from api.authentication.helpers import hash_password


async def add_user_to_db(db, user):
    """
    Функция для вставки ПользователяИ в талицу БД
    :param db: Объект сессии
    :param user: Данные
    :return: Добавленные данные
    """
    try:
        user_model = User(
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            login=user.login,
            password=hash_password(user.password),
            role=user.role,
            active=user.active,
            access_token=user.access_token,
            refresh_token=user.refresh_token)

        db.add(user_model)
        await db.commit()
        await db.refresh(user_model)
        print(user_model.password)

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
    users = await get_table_data(db, User)
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
        result = await db.execute(stmt)
        return result.scalars().all()
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")





