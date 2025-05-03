from typing import Annotated
from fastapi import Depends, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db
from db.students_list.db_commands import get_filtered_cards
from helpers.pagination import make_limit_dict

router = APIRouter()


@router.get('/students_cards',
            tags=['students list'],
            response_description="Карты студентов")
async def get_students_cards(  # token: str = Depends(get_current_active_auth_user),
                             skip: Annotated[int | None, Query()] = None,
                             limit: Annotated[int | None, Query()] = None,
                             firstname: Annotated[str | None, Query()] = None,
                             lastname: Annotated[str | None, Query()] = None,
                             faculty: Annotated[str | None, Query()] = None,
                             direction: Annotated[str | None, Query()] = None,
                             course: Annotated[str | None, Query()] = None,
                             department: Annotated[str | None, Query()] = None,
                             group: Annotated[str | None, Query()] = None,
                             subgroup: Annotated[str | None, Query()] = None,
                             session: AsyncSession = Depends(get_db)):
    """
    Используется для фильтрации и получения Карт студентов
    - skip: Пропускает заданное количество элементов
    - limit: Ограничивает количество возвращаемых элементов
    - firstname: Фильтр Имени
    - lastname: Фильтр Фамилии
    - faculty: Фильтр Факультета
    - direction: Фильтр Направления
    - course: Фильтр Курса обучения
    - department: Фильтр Кафедры
    - group: Фильтр Группы
    - subgroup: Фильтр Подгруппы
    """
    filters = {"personal_filters": {"firstname": firstname,
                                    "lastname": lastname},

               "educational_filters": {"faculty": faculty,
                                       "direction": direction,
                                       "course": course,
                                       "department": department,
                                       "group": group,
                                       "subgroup": subgroup}}

    students_cards = await get_filtered_cards(session, filters)
    limit_data = make_limit_dict(students_cards, skip, limit)
    return limit_data

