from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.user import add_user_to_db
from db.db_commands import get_db, change_data, delete_object, get_table_data
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
            response_model=list[UserSchemaOut],
            response_description="Список Пользователей")
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка пользователей
    """
    users = await get_table_data(db, User)
    return users


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






