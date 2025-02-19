from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_table_data, change_data, get_db, add_data_to_table, delete_object
from db.structure_commands import get_structures_data
from api.structure.fgos.models import FgosData
from api.structure.fgos.schemas import FgosIn, FgosOut


router = APIRouter()


@router.post("/fgos",
             tags=["fgos"],
             response_description="Добавленный ФГОС",
             response_model=FgosIn)
async def post_fgos(fgos: FgosIn,
                    db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления ФГОСа
    - fgos: Название ФГОСа
    """
    await add_data_to_table(db, fgos, FgosData)
    return fgos


@router.get("/fgos",
            tags=["fgos"],
            response_description="Список ФГОСов",
            response_model=list[FgosOut])
async def get_fgos(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка ФГОСов
    """
    data = await get_table_data(db, FgosData)
    return data


@router.get("/fgos/{fgos_id}",
            tags=["fgos"],
            response_description="ФГОС",
            response_model=list[FgosOut])
async def get_fgos(fgos_id: int,
                   db: AsyncSession = Depends(get_db)):
    """
    Используется для получения ФГОСа по идентификатору
    - fgos_id: Уникальный идентификатор ФГОСа
    """
    data = await get_table_data(db, FgosData, fgos_id)
    return data


@router.patch("/fgos/{fgos_id}",
              tags=['fgos'],
              response_description="Измененный ФГОС",
              response_model=list[FgosOut])
async def path_fgos(fgos_id: int,
                    parameters: dict = None,
                    db: AsyncSession = Depends(get_db)):
    """
    Используется для изменения параметров ФГОСа
    - fgos_id: Уникальный идентификатор ФГОСа
    - parameters: Новые данные
    """
    data = {"id": fgos_id,
            "table": FgosData,
            "parameters": parameters}

    updated_data = await change_data(db, data)
    return updated_data


@router.delete("/fgos/{fgos_id}",
               tags=['fgos'],
               response_description="Удаленный ФГОС")
async def delete_fgos(fgos_id: int,
                      db: AsyncSession = Depends(get_db)):
    """
    Используется для удаления ФГОСа
    - fgos_id: Уникальный идентификатор ФГОСа
    """
    result = await delete_object(db, fgos_id, FgosData)
    return result

