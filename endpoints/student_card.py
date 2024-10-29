from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from validation.auth_parameters import get_current_active_auth_user
from helpers.dicts import student_card_models_dict, student_card_validation_dict, student_params_validation_dict
from db.student_card_commands import change_card, delete_card, format_card_to_dict, add_commit_students_card
from db.db_commands import get_db
from schemas.student_card.students_card import StudentsCardSh
from fastapi.encoders import jsonable_encoder

from validation.student_card_parameters import validate_personal_data, validate_educational_data, validate_contact_data, \
    validate_other_data

router = APIRouter()


@router.post("/student_card", tags=['student card'])
async def post_student_card(student_card: StudentsCardSh,

                            db: AsyncSession = Depends(get_db)):
    student_card = await format_card_to_dict(student_card)

    for name_data, data in student_card.items():
        validation_function = student_card_validation_dict.get(name_data)
        if validation_function:
            validation_function(jsonable_encoder(data))

    result = await add_commit_students_card(db, student_card)
    return result


@router.patch("/change_student_card", tags=['student card'])
async def change_student_card(personal_id: int = None,
                              table_name: str = Query(enum=list(student_card_models_dict.keys())),
                              parameters: dict = None,
                              db: AsyncSession = Depends(get_db)):

    for parameter, new_val in parameters.items():
        validation_function = student_params_validation_dict.get(parameter)
        if validation_function:
            params = {"personal_id": personal_id,
                      "id": personal_id,
                      parameter: new_val}
            validation_function(params)

    data = {"personal_id": personal_id,
            "table_name": table_name,
            "parameters": parameters}

    updated_data = await change_card(db, data)
    return updated_data


@router.delete("/delete_student_card", tags=['student card'])
async def delete_student_card(token: str = Depends(get_current_active_auth_user),
                              personal_id: int = None,
                              db: AsyncSession = Depends(get_db)):
    result = await delete_card(db, personal_id)
    return result
