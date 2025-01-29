from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_table_data
from db.db_commands import get_db, add_data_to_table, delete_object
from db.structure_commands import get_structures_data, change_structure_data
from api.structure.group.models import GroupData
from api.structure.group.schemas import GroupIn, GroupOut


router = APIRouter()


@router.post("/group",
             tags=['group'],
             response_description="Добавленная Группа",
             response_model=GroupIn)
async def post_group(group: GroupIn,
                     db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Групп
    - group: Данные Групп
    """
    data = jsonable_encoder(group)
    list_of_groups = data.get('group')
    for gr in list_of_groups:
        data['group'] = gr
        await add_data_to_table(db, data, GroupData)

    return group


@router.get("/group",
            tags=["group"],
            response_description="Список Групп",
            response_model=list[GroupOut])
async def get_group(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка ФГОСов
    """
    data = await get_table_data(db, GroupData)
    return data


@router.get("/group/{group_id}",
            tags=["group"],
            response_description="Группа",
            response_model=list[GroupOut])
async def get_group(group_id: int,
                    db: AsyncSession = Depends(get_db)):
    """
    Используется для получения Группы по идентификатору
    - group_id: Уникальный идентификатор Группы
    """
    data = await get_table_data(db, GroupData, group_id)
    return data


@router.patch("/group/{group_id}",
              tags=['group'],
              response_description="Измененная Группа",
              response_model=list[GroupOut])
async def path_group(group_id: int,
                     parameters: dict = None,
                     db: AsyncSession = Depends(get_db)):
    """
    Используется для изменения параметров Группы
    - group_id: Уникальный идентификатор Группы
    - parameters: Новые данные
    """
    data = {"id": group_id,
            "table": GroupData,
            "parameters": parameters}

    updated_data = await change_structure_data(db, data)
    return updated_data


@router.delete("/group/{group_id}",
               tags=['group'],
               response_description="Удаленная Группа")
async def delete_group(group_id: int,
                       db: AsyncSession = Depends(get_db)):
    """
    Используется для удаления Группы
    - group_id: Уникальный идентификатор Группы
    """
    result = await delete_object(db, group_id, GroupData)
    return result

