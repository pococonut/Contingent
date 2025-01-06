from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from validation.auth_parameters import get_current_active_auth_user
from helpers.dicts import all_models_dict
from db.db_commands import get_db, add_data_to_table, get_table_data

router = APIRouter()


@router.get("/create_db",
            tags=["database"],
            response_description="Сообщение об успешном создании БД")
async def create_db(db: AsyncSession = Depends(get_db)):
    """
    Используется для создания БД
    """
    return {"result": "database was created"}