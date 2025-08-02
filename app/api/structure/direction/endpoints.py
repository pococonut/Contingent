from fastapi import Depends, APIRouter
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_table_data, change_data, get_db, add_data_to_table, delete_object, get_table_data_paginate
from api.structure.direction.models import DirectionData
from api.structure.direction.schemas import DirectionIn, DirectionOut
from validation.auth_parameters import get_current_active_auth_user


router = APIRouter()


@router.post("/direction",
             tags=["direction"],
             response_description="Добавленное Направление обучения",
             response_model=DirectionIn)
async def post_direction(direction: DirectionIn,
                         db: AsyncSession = Depends(get_db),
                         token: str = Depends(get_current_active_auth_user)):
    """
    Используется для добавления Направления обучения
    - direction: Название Направления обучения
    """
    await add_data_to_table(db, direction, DirectionData)
    return direction


@router.get("/direction",
            tags=["direction"],
            response_description="Список Направлений обучения",
            response_model=Page[DirectionOut])
async def get_direction(db: AsyncSession = Depends(get_db),
                        token: str = Depends(get_current_active_auth_user)):
    """
    Используется для получения списка Направлений обучения
    """
    data = await get_table_data_paginate(db, DirectionData)
    return data


@router.get("/direction/{direction_id}",
            tags=["direction"],
            response_description="Направление обучения",
            response_model=list[DirectionOut])
async def get_direction(direction_id: int,
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(get_current_active_auth_user)):
    """
    Используется для получения Направления обучения по идентификатору
    """
    data = await get_table_data(db, DirectionData, direction_id)
    return data


@router.patch("/direction/{direction_id}",
              tags=['direction'],
              response_description="Измененное Направление обучения",
              response_model=list[DirectionOut])
async def path_direction(direction_id: int,
                         parameters: dict = None,
                         db: AsyncSession = Depends(get_db),
                         token: str = Depends(get_current_active_auth_user)):
    """
    Используется для изменения параметров Направления
    - direction_id: Уникальный идентификатор Направления
    - parameters: Новые данные
    """
    data = {"id": direction_id,
            "table": DirectionData,
            "parameters": parameters}

    updated_data = await change_data(db, data)
    return updated_data


@router.delete("/direction/{direction_id}",
               tags=['direction'],
               response_description="Удаленное Направление обучения")
async def delete_direction(direction_id: int,
                           db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_current_active_auth_user)):
    """
    Используется для удаления Направления
    - direction_id: Уникальный идентификатор Направления
    """
    result = await delete_object(db, direction_id, DirectionData)
    return result

