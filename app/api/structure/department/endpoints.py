from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_table_data
from db.db_commands import get_db, add_data_to_table, delete_object
from db.structure_commands import get_structures_data, change_structure_data
from api.structure.department.models import DepartmentData
from api.structure.department.schemas import DepartmentSh


router = APIRouter()


@router.post("/department",
             tags=["department"],
             response_description="Добавленная Кафедра")
async def post_department(department: DepartmentSh,
                          db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Кафедры
    - department: Название Направления обучения
    """
    await add_data_to_table(db, department, DepartmentData)
    return {"Successfully added": department}


@router.get("/department",
            tags=["department"],
            response_description="Список Кафедр")
async def get_department(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения списка Кафедр
    """
    data = await get_table_data(db, DepartmentData)
    return data


@router.get("/department/{department_id}",
            tags=["department"],
            response_description="Кафедра")
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
              response_description="Измененное Кафедра")
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

    updated_data = await change_structure_data(db, data)
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

