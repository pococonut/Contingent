from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db
from db.user import add_user_to_db
from db.db_commands import get_table_data
from api.user.schemas import UserSchema, UserSchemaOut
from api.user.models import User

router = APIRouter()


@router.post("/user",
             tags=["user"],
             response_model=UserSchemaOut)
async def post_user(user: UserSchema,
                    db: AsyncSession = Depends(get_db)):
    """
    Используется для вставки данных о пользователе
    """
    await add_user_to_db(db, user)
    return user


@router.get("/users",
            tags=['user'],
            response_model=list[UserSchemaOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка пользователей
    """
    users = await get_table_data(db, User)
    return users

