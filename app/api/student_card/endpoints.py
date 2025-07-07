from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.student_card.models.personal import PersonalData
from helpers.dicts import student_card_models_dict, student_card_validation_dict, student_params_validation_dict
from db.student_card.db_commands import change_card, format_card_to_dict, add_commit_students_card, get_cards, get_card
from db.db_commands import get_db, delete_object
from api.student_card.schemas.students_card import StudentsCardSh

from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/student_card",
             tags=['student card'],
             response_description="Добавленная Карта студента")
async def post_student_card(student_card: StudentsCardSh,
                            db: AsyncSession = Depends(get_db)):
    """
    Используется для добавления Карты студента
    - student_card: Карта студента
    """
    student_card = await format_card_to_dict(student_card)
    for name_data, data in student_card.items():
        validation_function = student_card_validation_dict.get(name_data)
        if validation_function:
            validation_function(jsonable_encoder(data))

    await add_commit_students_card(db, student_card)
    return student_card


@router.get("/students_cards",
            tags=['student card'],
            response_description="Карты студентов")
async def get_students_card(db: AsyncSession = Depends(get_db)):
    """
    Используется для получения Карт студентов
    """
    student_cards = await get_cards(db)
    return student_cards


@router.get("/student_card/{personal_id}",
            tags=['student card'],
            response_description="Карта студента")
async def get_students_card(personal_id: int,
                            db: AsyncSession = Depends(get_db)):
    """
    Используется для получения Карт студентов
    """
    student_cards = await get_card(db, personal_id)
    return student_cards


@router.patch("/student_card/{personal_id}",
              tags=['student card'],
              response_description="Измененная Карта студента")
async def change_student_card(personal_id: int,
                              table_name: str = Query(enum=list(student_card_models_dict.keys())),
                              parameters: dict = None,
                              db: AsyncSession = Depends(get_db)):
    """
    Используется для изменения Карты студента
    - personal_id: Идентификатор студента
    - table_name: Названия таблицы БД
    - parameters: Новые значения параметров Карты студента
    """
    # Валидация
    # for parameter, new_val in parameters.items():
    #     validation_function = student_params_validation_dict.get(parameter)
    #     if validation_function:
    #         params = {"personal_id": personal_id,
    #                   "id": personal_id,
    #                   parameter: new_val}
    #         validation_function(params)

    data = {"personal_id": personal_id,
            "table_name": table_name,
            "parameters": parameters}

    updated_data = await change_card(db, data)
    return updated_data


@router.delete("/student_card/{personal_id}",
               tags=['student card'],
               response_description="Сообщение об успешном удалении")
async def delete_student_card(personal_id: int = None,
                              db: AsyncSession = Depends(get_db)):
    """
    Используется для удаления Карты студента
    - personal_id: Идентификатор студента
    """
    result = await delete_object(db, personal_id, PersonalData)
    return result
