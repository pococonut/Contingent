from typing import Annotated, List
from fastapi import Depends, Query, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data_to_table, get_table_data
from db.students_list.db_commands import get_filtered_cards
from helpers.pagination import make_limit_list
from api.students_list.number_contingent.models import PlannedNumContingent
from api.students_list.number_contingent.schemas import PlannedNumContingentSh
from api.students_list.number_contingent.helpers import get_students_number_contingent
from validation.auth_parameters import get_current_active_auth_user

router = APIRouter()


@router.get("/current_number_contingent",
            tags=['students list'],
            response_description="Численный список студентов")
async def get_number_contingent(# token: str = Depends(get_current_active_auth_user),
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
                                session: AsyncSession = Depends(get_db),
                                token: str = Depends(get_current_active_auth_user)
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
                                db: AsyncSession = Depends(get_db),
                                token: str = Depends(get_current_active_auth_user)):
    """
    Используется для добавления планируемого численного списка студентов
    - number_lists: Список словарей, содержащих данные планируемого численного списка по направлениям
    """
    for lst in number_lists:
        await add_data_to_table(db, lst, PlannedNumContingent)
    return {"Successfully added": number_lists}


@router.get("/planned_number_contingent",
            tags=['students list'],
            response_description="Планируемый численный список студентов",
            response_model=List[PlannedNumContingentSh])
async def get_planned_num_list(db: AsyncSession = Depends(get_db),
                               token: str = Depends(get_current_active_auth_user)):
    """
    Используется для получения планируемого численного списка студентов
    - skip: Пропускает заданное количество элементов
    - limit: Ограничивает количество возвращаемых элементов
    """
    planned_contingent = await get_table_data(db, PlannedNumContingent)
    return jsonable_encoder(planned_contingent)
