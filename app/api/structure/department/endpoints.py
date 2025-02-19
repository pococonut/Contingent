from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_table_data, get_db, add_data_to_table, delete_object, change_data
from db.structure_commands import get_structures_data
from api.structure.department.models import DepartmentData
from api.structure.department.schemas import DepartmentIn, DepartmentOut


router = APIRouter()


@router.post("/department",
             tags=["department"],
             response_description="Добавленная Кафедра",
             response_model=DepartmentIn)
async def post_department(department: DepartmentIn,
                          db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Кафедры
    - department: Название Направления обучения
    """
    await add_data_to_table(db, department, DepartmentData)
    return department


@router.get("/department",
            tags=["department"],
            response_description="Список Кафедр",
            response_model=list[DepartmentOut])
async def get_department(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка Кафедр
    """
    data = await get_table_data(db, DepartmentData)
    return data


@router.get("/department/{department_id}",
            tags=["department"],
            response_description="Кафедра",
            response_model=list[DepartmentOut])
async def get_department(department_id: int,
                         db: AsyncSession = Depends(get_db)):
    """
    Используется для получения Кафедры по идентификатору
    - department_id: Уникальный идентификатор Кафедры
    """
    data = await get_table_data(db, DepartmentData, department_id)
    return data


@router.patch("/department/{department_id}",
              tags=["department"],
              response_description="Измененное Кафедра",
              response_model=list[DepartmentOut])
async def path_department(department_id: int,
                          parameters: dict = None,
                          db: AsyncSession = Depends(get_db)):
    """
    Используется для изменения параметров Кафедры
    - department_id: Уникальный идентификатор Кафедры
    - parameters: Новые данные
    """
    data = {"id": department_id,
            "table": DepartmentData,
            "parameters": parameters}

    updated_data = await change_data(db, data)
    return updated_data


@router.delete("/department/{department_id}",
               tags=["department"],
               response_description="Удаленная Кафедра")
async def delete_department(department_id: int,
                            db: AsyncSession = Depends(get_db)):
    """
    Используется для удаления Кафедры
    - department_id: Уникальный идентификатор Кафедры
    """
    result = await delete_object(db, department_id, DepartmentData)
    return result

