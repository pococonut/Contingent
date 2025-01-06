import logging

from fastapi import HTTPException
from sqlalchemy import select, update, exc

from helpers.dicts import structure_models_dict
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
                   SubgroupData.direction,
                   SubgroupData.profile,
                   SubgroupData.course,
                   SubgroupData.group,
                   GroupData.fgos,
                   DirectionData.short_name,
                   DirectionData.number,
                   DirectionData.qualification,
                   DirectionData.form)
            .join(GroupData, GroupData.group == SubgroupData.group)
            .join(DirectionData, SubgroupData.direction == DirectionData.direction).distinct())

    parameters = ["id",
                  "subgroup",
                  "direction",
                  "profile",
                  "course",
                  "group",
                  "fgos",
                  "short_name",
                  "number",
                  "qualification",
                  "form"]

    try:
        result = await db.execute(stmt)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"SQLAlchemyError: {e}")

    data = []
    for row in result:
        row_data = dict((name, row[idx]) for idx, name in enumerate(parameters))
        data.append(row_data)

    return data


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

    except exc.SQLAlchemyError as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"SQLAlchemyError: {e}")
