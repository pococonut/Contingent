from typing import Annotated
from fastapi import Depends, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db
from db.filtering_cards_commands import get_filtered_cards
from validation.auth_parameters import get_current_active_auth_user
from helpers.number_contingent import get_students_number_contingent

router = APIRouter()


@router.get('/students_cards',
            tags=['students list'],
            response_description="Карты студентов")
async def get_students_cards(token: str = Depends(get_current_active_auth_user),
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
    return students_cards


@router.get("/number_contingent",
            tags=['students list'],
            response_description="Численный список студентов")
async def get_number_contingent(token: str = Depends(get_current_active_auth_user),
                                firstname: Annotated[str | None, Query()] = None,
                                lastname: Annotated[str | None, Query()] = None,
                                faculty: Annotated[str | None, Query()] = None,
                                direction: Annotated[str | None, Query()] = None,
                                course: Annotated[str | None, Query()] = None,
                                department: Annotated[str | None, Query()] = None,
                                group: Annotated[str | None, Query()] = None,
                                subgroup: Annotated[str | None, Query()] = None,
                                session: AsyncSession = Depends(get_db),

                                ):
    """
    Используется для фильтрации и получения численного списка студентов
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
    number_contingent = await get_students_number_contingent(students_cards)
    return number_contingent

