from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from validation.auth_parameters import get_current_active_auth_user
from general.dicts import models_dict
from db.db_commands import get_db


router = APIRouter()


@router.get("/table_data")
async def get_table_data(token: str = Depends(get_current_active_auth_user),
                         table_name: str = Query(enum=list(models_dict.keys())),
                         db: AsyncSession = Depends(get_db)):
    table = models_dict.get(table_name)
    result = await db.execute(select(table))
    data = result.scalars().all()
    return {f"{table_name}": data}


@router.get("/create_db")
async def create_db(db: AsyncSession = Depends(get_db)):
    return {"result": "database was created"}
