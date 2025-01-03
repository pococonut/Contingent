from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_table_data
from db.db_commands import get_db, add_data_to_table, delete_object
from db.structure_commands import get_structures_data, change_structure_data
from api.structure.profile.models import ProfileData
from api.structure.profile.schemas import ProfileSh


router = APIRouter()


@router.post("/profile",
             tags=["profile"],
             response_description="Добавленный Профиль")
async def post_profile(profile: ProfileSh,
                    db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Профиля
    - profile: Название ФГОСа
    """
    await add_data_to_table(db, profile, ProfileData)
    return {"Successfully added": profile}


@router.get("/profile",
            tags=["profile"],
            response_description="Список Профилей")
async def get_profile(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка Профилей
    """
    data = await get_table_data(db, ProfileData)
    return data


@router.get("/profile/{profile_id}",
            tags=["profile"],
            response_description="Профиль")
async def get_profile(profile_id: int,
                   db: AsyncSession = Depends(get_db)):
    """
    Используется для получения Профиля по идентификатору
    - profile_id: Уникальный идентификатор Профиля
    """
    data = await get_table_data(db, ProfileData, profile_id)
    return data


@router.patch("/profile/{profile_id}",
              tags=['profile'],
              response_description="Измененный Профиль")
async def path_profile(profile_id: int,
                       parameters: dict = None,
                       db: AsyncSession = Depends(get_db)):
    """
    Используется для изменения параметров Профиля
    - profile_id: Уникальный идентификатор Профиля
    - parameters: Новые данные
    """
    data = {"id": profile_id,
            "table": ProfileData,
            "parameters": parameters}

    updated_data = await change_structure_data(db, data)
    return updated_data


@router.delete("/profile/{profile_id}",
               tags=['profile'],
               response_description="Удаленный Профиль")
async def delete_profile(profile_id: int,
                         db: AsyncSession = Depends(get_db)):
    """
    Используется для удаления Профиля
    - profile_id: Уникальный идентификатор Профиля
    """
    result = await delete_object(db, profile_id, ProfileData)
    return result

