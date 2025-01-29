from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data_to_table, delete_object
from db.structure_commands import get_structures_data, change_structure_data
from helpers.pagination import make_limit_list
from api.structure.structure.schemas import StructureOut

router = APIRouter()


@router.get("/structure",
            tags=['structure'],
            response_description="Данные Структур",
            response_model=list[StructureOut])
async def get_structures(skip: int = 0,
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


