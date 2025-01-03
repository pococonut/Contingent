from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from validation.auth_parameters import get_current_active_auth_user
from helpers.dicts import all_models_dict
from db.db_commands import get_db, add_data_to_table, get_table_data

router = APIRouter()


@router.get("/create_db",
            tags=["database"],
            response_description="Сообщение об успешном создании БД")
async def create_db(db: AsyncSession = Depends(get_db),
                    token: str = Depends(get_current_active_auth_user)):
    """
    Используется для создания БД
    """
    return {"result": "database was created"}


@router.get("/table_data",
            tags=["database"],
            response_description="Данные таблицы БД")
async def get_table(db: AsyncSession = Depends(get_db),
                    table_name: str = Query(enum=list(all_models_dict.keys()))):
    """
    Используется для получения данных таблицы БД
    - table_name: Название таблицы БД
    """
    table = all_models_dict.get(table_name)
    data = await get_table_data(db, table)
    return {f"{table_name}": data}


@router.post("/table_data",
             tags=["database"],
             response_description="Добавленные в таблицу БД данные")
async def post_table(data: dict,
                     token: str = Depends(get_current_active_auth_user),
                     table_name: str = Query(enum=list(all_models_dict.keys())),
                     db: AsyncSession = Depends(get_db)):
    """
    Используется для добавление данных в таблицу БД
    - data: Данные для добавления в таблицу БД
    - table_name: Название таблицы БД
    """
    await add_data_to_table(db, data, all_models_dict.get(table_name))
    return {"Successfully added": data}
