import logging

from sqlalchemy import select, update

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
                   SubgroupData.course,
                   SubgroupData.group_name,
                   GroupData.fgos,
                   DirectionData.short_name,
                   DirectionData.number,
                   DirectionData.qualification,
                   DirectionData.form)
            .join(GroupData, GroupData.name == SubgroupData.group_name)
            .join(DirectionData, SubgroupData.direction_name == DirectionData.name))

    result = await db.execute(stmt)
    data = []

    for row in result:
        data.append({
            "id": row[0],
            "subgroup_name": row[1],
            "direction_name": row[2],
            "course": row[3],
            "group_name": row[4],
            "fgos": row[5],
            "short_name": row[6],
            "number": row[7],
            "qualification": row[8],
            "form": row[9]
        })

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
    parameters = data.get("parameters")
    table = structure_models_dict.get("subgroup")
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

    except Exception as e:
        logging.error(e)


