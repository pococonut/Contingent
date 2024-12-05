from fastapi import Depends, APIRouter, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data_to_table, delete_object
from db.structure_commands import get_structures_data, change_structure
from helpers.pagination import make_limit_list
from helpers.dicts import structure_models_dict
from models.structure.direction import DirectionData
from models.structure.department import DepartmentData
from models.structure.fgos import FgosData
from models.structure.group import GroupData
from models.structure.profile import ProfileData
from models.structure.subgroup import SubgroupData
from schemas.structure.direction import DirectionSh
from schemas.structure.department import DepartmentSh
from schemas.structure.group import GroupSh
from schemas.structure.profile import ProfileSh
from schemas.structure.subgroup import SubgroupSh
from schemas.structure.fgos import FgosSh
from validation.auth_parameters import get_current_active_auth_user

router = APIRouter()


@router.post("/direction",
             tags=['structure'],
             response_description="Добавленное Направление обучения")
async def post_direction(direction: DirectionSh,
                         token: str = Depends(get_current_active_auth_user),
                         db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Направления обучения
    - direction: Название Направления обучения
    """
    await add_data_to_table(db, direction, DirectionData)
    return {"Successfully added": direction}


@router.post("/department",
             tags=['structure'],
             response_description="Добавленная Кафедра направления")
async def post_department(department: DepartmentSh,
                          token: str = Depends(get_current_active_auth_user),
                          db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Кафедры направления
    - department: Название Кафедры направления
    """
    await add_data_to_table(db, department, DepartmentData)
    return {"Successfully added": department}


@router.post("/profile",
             tags=['structure'],
             response_description="Добавленный Профиль обучения")
async def post_profile(profile: ProfileSh,
                       token: str = Depends(get_current_active_auth_user),
                       db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Профиля обучения
    - profile: Название Профиля обучения
    """
    await add_data_to_table(db, profile, ProfileData)
    return {"Successfully added": profile}


@router.post("/fgos",
             tags=['structure'],
             response_description="Добавленный ФГОС")
async def post_profile(fgos: FgosSh,
                       token: str = Depends(get_current_active_auth_user),
                       db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления ФГОСа направления
    - fgos: Название ФГОСа направления
    """
    await add_data_to_table(db, fgos, FgosData)
    return {"Successfully added": fgos}


@router.post("/group",
             tags=['structure'],
             response_description="Добавленная Группа")
async def post_group(group: GroupSh,
                     token: str = Depends(get_current_active_auth_user),
                     db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Групп и их данных
    - group: Данные Групп
    """
    data = jsonable_encoder(group)
    list_of_groups = data.get('name')
    for gr in list_of_groups:
        data['name'] = gr
        await add_data_to_table(db, data, GroupData)

    return {"Successfully added": group}


@router.post("/subgroup",
             tags=['structure'],
             response_description="Добавленная Подгруппа")
async def post_subgroup(subgroup: SubgroupSh,
                        token: str = Depends(get_current_active_auth_user),
                        db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Подгрупп и их данных
    - group: Данные Подгрупп
    """
    data = jsonable_encoder(subgroup)
    list_of_subgroups = data.get('name')

    for sgr in list_of_subgroups:
        data['name'] = sgr
        await add_data_to_table(db, data, SubgroupData)

    return {"Successfully added": subgroup}


@router.get("/structures",
            tags=['structure'],
            response_description="Данные Структур")
async def get_structures(token: str = Depends(get_current_active_auth_user),
                         skip: int = 0,
                         limit: int = 10,
                         db: AsyncSession = Depends(get_db)):
    """
    Используется для получения Структур
    - skip: Пропускает заданное количество элементов
    - limit: Ограничивает количество возвращаемых элементов
    """
    data = await get_structures_data(db)
    limit_data = make_limit_list(data, skip, limit)
    return limit_data


@router.patch("/structure",
              tags=['structure'],
              response_description="Обновленные данные Структуры")
async def change_change_structure(token: str = Depends(get_current_active_auth_user),
                                  structure_id: int = None,
                                  table_name: str = Query(enum=list(structure_models_dict.keys())),
                                  parameters: dict = None,
                                  db: AsyncSession = Depends(get_db)):
    """
    Используется для изменения параметров Структуры
    - structure_id: Уникальный идентификатор Структуры
    - table_name: Название таблицы БД
    - parameters: Новые данные
    """
    data = {"structure_id": structure_id,
            "table_name": table_name,
            "parameters": parameters}

    updated_data = await change_structure(db, data)
    return updated_data


@router.delete("/structure",
               tags=['structure'],
               response_description="Удаление данных Структуры")
async def remove_structure(structure_id: int = None,
                           token: str = Depends(get_current_active_auth_user),
                           table_name: str = Query(enum=list(structure_models_dict.keys())),
                           db: AsyncSession = Depends(get_db)):
    """
    Используется для удаления Структуры
    - structure_id: Уникальный идентификатор Структуры
    - table_name: Название таблицы БД
    """
    table = structure_models_dict.get(table_name)
    result = await delete_object(db, structure_id, table)
    return result
