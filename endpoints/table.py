from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from validation.auth_parameters import get_current_active_auth_user
from helpers.dicts import all_models_dict
from db.db_commands import get_db, add_data_to_table

router = APIRouter()


@router.get("/table_data", tags=["database"])
async def get_table_data(table_name: str = Query(enum=list(all_models_dict.keys())),
                         db: AsyncSession = Depends(get_db)):
    table = all_models_dict.get(table_name)
    result = await db.execute(select(table))
    data = result.scalars().all()
    return {f"{table_name}": data}


@router.get("/create_db", tags=["database"])
async def create_db(db: AsyncSession = Depends(get_db)):
    return {"result": "database was created"}


@router.post("/table_data", tags=["database"])
async def get_table_data(data: dict,
                         table_name: str = Query(enum=list(all_models_dict.keys())),
                         db: AsyncSession = Depends(get_db)):
    await add_data_to_table(db, data, all_models_dict.get(table_name))
    return {"Successfully added": data}