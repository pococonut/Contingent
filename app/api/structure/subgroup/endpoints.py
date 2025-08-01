from fastapi import Depends, APIRouter
from fastapi_pagination import Page
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_table_data, get_table_data_paginate, change_data, get_db, add_data_to_table, delete_object
from api.structure.subgroup.models import SubgroupData
from api.structure.subgroup.schemas import SubgroupIn, SubgroupOut
from validation.auth_parameters import get_current_active_auth_user

router = APIRouter()


@router.post("/subgroup",
             tags=['subgroup'],
             response_description="Добавленная Подгруппа",
             response_model=SubgroupIn)
async def post_subgroup(subgroup: SubgroupIn,
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(get_current_active_auth_user)):
    """
    Используется для добавления Подгрупп и их данных
    - subgroup: Данные Подгрупп
    """
    data = jsonable_encoder(subgroup)
    list_of_subgroups = data.get('subgroup')

    for sgr in list_of_subgroups:
        data['subgroup'] = sgr
        await add_data_to_table(db, data, SubgroupData)

    return subgroup


@router.get("/subgroup",
            tags=["subgroup"],
            response_description="Список Подгрупп",
            response_model=Page[SubgroupOut])
async def get_subgroup(db: AsyncSession = Depends(get_db),
                       token: str = Depends(get_current_active_auth_user)):
    """
    Используется для получения списка Подгрупп
    """
    data = await get_table_data_paginate(db, SubgroupData)
    return data


@router.get("/subgroup/{subgroup_id}",
            tags=["subgroup"],
            response_description="Подгруппа",
            response_model=list[SubgroupOut])
async def get_subgroup(subgroup_id: int,
                       db: AsyncSession = Depends(get_db),
                       token: str = Depends(get_current_active_auth_user)):
    """
    Используется для получения Подгруппы по идентификатору
    - subgroup_id: Уникальный идентификатор ФГОСа
    """
    data = await get_table_data(db, SubgroupData, subgroup_id)
    return data


@router.patch("/subgroup/{subgroup_id}",
              tags=['subgroup'],
              response_description="Измененная Подгруппа",
              response_model=list[SubgroupOut])
async def path_subgroup(subgroup_id: int,
                        parameters: dict = None,
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(get_current_active_auth_user)):
    """
    Используется для изменения параметров Подгруппы
    - subgroup_id: Уникальный идентификатор Подгруппы
    - parameters: Новые данные
    """
    data = {"id": subgroup_id,
            "table": SubgroupData,
            "parameters": parameters}

    updated_data = await change_data(db, data)
    return updated_data


@router.delete("/subgroup/{subgroup_id}",
               tags=['subgroup'],
               response_description="Удаленная Подгруппа")
async def delete_subgroup(subgroup_id: int,
                          db: AsyncSession = Depends(get_db),
                          token: str = Depends(get_current_active_auth_user)):
    """
    Используется для удаления Подгруппы
    - subgroup_id: Уникальный идентификатор Подгруппы
    """
    result = await delete_object(db, subgroup_id, SubgroupData)
    return result

