from fastapi import Depends, APIRouter
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db
from db.structure.db_commands import get_structures_data
from api.structure.structure.schemas import StructureOut
from validation.auth_parameters import get_current_active_auth_user

router = APIRouter()


@router.get("/structure",
            tags=['structure'],
            response_description="Данные Структур",
            response_model=Page[StructureOut])
async def get_structures(db: AsyncSession = Depends(get_db),
                         token: str = Depends(get_current_active_auth_user)):
    """
    Используется для получения Структур
    - skip: Пропускает заданное количество элементов
    - limit: Ограничивает количество возвращаемых элементов
    """
    data = await get_structures_data(db)
    return data


