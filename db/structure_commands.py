from sqlalchemy import select

from models.structure.direction import DirectionData
from models.structure.group import GroupData
from models.structure.subgroup import SubgroupData


async def get_structures_data(db):
    """
    Функция для получения Структур
    :param db: Объект сессии
    :return: Список структур
    """
    stmt = (select(SubgroupData.name,
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
            "subgroup_name": row[0],
            "direction_name": row[1],
            "course": row[2],
            "group_name": row[3],
            "fgos": row[4],
            "short_name": row[5],
            "number": row[6],
            "qualification": row[7],
            "form": row[8]
        })

    return data
