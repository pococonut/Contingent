from fastapi import Depends, APIRouter
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from db.user import add_user_to_db, get_user_by_name
from db.db_commands import get_db, change_data, delete_object, get_table_data_paginate, get_table_data
from api.user.schemas import UserSchema, UserSchemaOut
from api.user.models import User

router = APIRouter()


@router.post("/user",
             tags=["user"],
             response_model=UserSchemaOut,
             response_description="Добавленный Пользователь")
async def post_user(user: UserSchema,
                    db: AsyncSession = Depends(get_db)):
    """
    Используется для вставки данных о пользователе
    """
    await add_user_to_db(db, user)
    return user


@router.get("/users",
            tags=['user'],
            response_model=Page[UserSchemaOut],
            response_description="Список Пользователей")
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка пользователей
    """
    users = await get_table_data_paginate(db, User)
    return users


@router.get("/user/{user_id}",
            tags=['user'],
            response_model=list[UserSchemaOut],
            response_description="Пользователь")
async def get_user_id(user_id: int,
                      db: AsyncSession = Depends(get_db)):
    """
    Используется для получения данных Пользователя по идентификатору
    """
    user = await get_table_data(db, User, user_id)
    return user


@router.get("/user_by_name",
            tags=['user'],
            response_model=Page[UserSchemaOut],
            response_description="Список Пользователей")
async def get_user_name(first_name: str,
                        last_name: str,
                        middle_name: str | None = None,
                        db: AsyncSession = Depends(get_db)):
    """
    Используется для получения данных Пользователя по ФИО
    """
    user_name = {"first_name": first_name,
                 "last_name": last_name,
                 "middle_name": middle_name}
    user = await get_user_by_name(db, user_name)
    return user


@router.patch("/user/{user_id}",
              tags=['user'],
              response_model=list[UserSchemaOut],
              response_description="Измененный Пользователь")
async def change_user(user_id: int,
                      parameters: dict = None,
                      db: AsyncSession = Depends(get_db)):
    """
    Используется для изменения параметров Пользователя
    - user_id: Уникальный идентификатор Пользователя
    - parameters: Новые данные
    """
    data = {"id": user_id,
            "table": User,
            "parameters": parameters}

    updated_data = await change_data(db, data)
    return updated_data


@router.delete("/user/{user_id}",
               tags=["user"],
               response_description="Удаленный Пользователь")
async def delete_department(user_id: int,
                            db: AsyncSession = Depends(get_db)):
    """
    Используется для удаления Кафедры
    - department_id: Уникальный идентификатор Кафедры
    """
    result = await delete_object(db, user_id, User)
    return result






