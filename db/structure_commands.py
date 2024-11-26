import logging

from fastapi import HTTPException
from sqlalchemy import select, update, exc

from helpers.dicts import structure_models_dict
from models.structure.direction import DirectionData
from models.structure.group import GroupData
from models.structure.subgroup import SubgroupData


async def get_structures_data(db):
    """
    Функция для получения Структур
    :param db: Объект сессии
    :return: Список Структур
    """
    stmt = (select(SubgroupData.id,
                   SubgroupData.name,
                   SubgroupData.direction_name,
                   SubgroupData.profile_name,
                   SubgroupData.course,
                   SubgroupData.group_name,
                   GroupData.fgos,
                   DirectionData.short_name,
                   DirectionData.number,
                   DirectionData.qualification,
                   DirectionData.form)
            .join(GroupData, GroupData.name == SubgroupData.group_name)
            .join(DirectionData, SubgroupData.direction_name == DirectionData.name).distinct())

    parameters = ["id",
                  "subgroup_name",
                  "direction_name",
                  "profile_name",
                  "course",
                  "group_name",
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


async def change_structure(db, data):
    """
    Функция для изменения Структуры
    :param db: Объект сессии
    :param data: Словарь, содержащий имя таблицы,
     параметры для изменения, идентификатор Структуры
    :return: Измененная Структура
    """
    structure_id = data.get("structure_id")
    table_name = data.get("table_name")
    parameters = data.get("parameters")
    table = structure_models_dict.get(table_name)
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
