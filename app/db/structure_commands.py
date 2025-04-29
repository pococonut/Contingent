import logging

from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, update, exc

from api.structure.direction.models import DirectionData
from api.structure.group.models import GroupData
from api.structure.subgroup.models import SubgroupData


async def get_structures_data(db):
    """
    Функция для получения Структур
    :param db: Объект сессии
    :return: Список Структур
    """
    stmt = (select(SubgroupData.id,
                   SubgroupData.subgroup,
                   SubgroupData.profile,
                   SubgroupData.group,
                   GroupData.course,
                   GroupData.direction,
                   DirectionData.code,
                   DirectionData.qualification,
                   DirectionData.education_form)
            .join(GroupData, GroupData.group == SubgroupData.group)
            .join(DirectionData, GroupData.direction == DirectionData.name).distinct())

    try:
        result = await paginate(db, stmt)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")
    return result


async def change_structure_data(db, data):
    """
    Функция для изменения Структуры
    :param db: Объект сессии
    :param data: Словарь, содержащий имя таблицы,
     параметры для изменения, идентификатор Структуры
    :return: Измененная Структура
    """
    structure_id = data.get("id")
    table = data.get("table")
    parameters = data.get("parameters")
    structure_id_db = table.id

    try:
        for parameter, new_val in parameters.items():
            stmt = update(table).where(structure_id_db == structure_id)
            stmt = stmt.values({f"{parameter}": new_val})
            await db.execute(stmt)
        await db.commit()

        stmt = select(table).where(structure_id_db == structure_id)
        result = await db.execute(stmt)
        updated_data = result.scalars().all()
        return updated_data
    except exc.IntegrityError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"IntegrityError: AlreadyExists")
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQLAlchemyError: {e}")
