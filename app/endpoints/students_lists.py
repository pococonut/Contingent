from typing import Annotated
from fastapi import Depends, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data_to_table, get_table_data
from db.filtering_cards_commands import get_filtered_cards
from helpers.pagination import make_limit_dict, make_limit_list
from models.student_list.planned_num_contingent import PlannedNumContingent
from validation.auth_parameters import get_current_active_auth_user
from helpers.number_contingent import get_students_number_contingent, get_rid_of_ids
from schemas.student_list.planned_num_contingent import PlannedNumContingentSh

router = APIRouter()


@router.get('/students_cards',
            tags=['students list'],
            response_description="Карты студентов")
async def get_students_cards(token: str = Depends(get_current_active_auth_user),
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


@router.get("/current_number_contingent",
            tags=['students list'],
            response_description="Численный список студентов")
async def get_number_contingent(token: str = Depends(get_current_active_auth_user),
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
                                session: AsyncSession = Depends(get_db)
                                ):
    """
    Используется для фильтрации и получения численного списка студентов
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
    number_contingent = get_students_number_contingent(students_cards)
    limit_data = make_limit_list(number_contingent, skip, limit)
    return limit_data


@router.post("/planned_number_contingent",
             tags=['students list'],
             response_description="Добавленный планируемый численный список студентов")
async def post_planned_num_list(number_lists: list[PlannedNumContingentSh],
                                token: str = Depends(get_current_active_auth_user),
                                db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления планируемого численного списка студентов
    - number_lists: Список словарей, содержащих данные планируемого численного списка по направлениям
    """
    for lst in number_lists:
        await add_data_to_table(db, lst, PlannedNumContingent)
    return {"Successfully added": number_lists}


@router.get("/planned_number_contingent",
            tags=['students list'],
            response_description="Планируемый численный список студентов")
async def get_planned_num_list(token: str = Depends(get_current_active_auth_user),
                               skip: Annotated[int | None, Query()] = None,
                               limit: Annotated[int | None, Query()] = None,
                               db: AsyncSession = Depends(get_db)):
    """
    Используется для получения планируемого численного списка студентов
    - skip: Пропускает заданное количество элементов
    - limit: Ограничивает количество возвращаемых элементов
    """
    planned_contingent = await get_table_data(db, PlannedNumContingent)
    without_ids = get_rid_of_ids(planned_contingent)
    limit_data = make_limit_list(without_ids, skip, limit)
    return limit_data
