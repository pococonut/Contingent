from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from validation.auth_parameters import get_current_active_auth_user
from general.dicts import models_dict
from db.db_commands import get_db, change_card, delete_card, format_card_to_dict, add_commit_students_card
from schemas.student_card.students_card import StudentsCardSh
from fastapi.encoders import jsonable_encoder

from validation.student_card_parameters import validate_personal_data, validate_educational_data, validate_contact_data, \
    validate_other_data

router = APIRouter()


@router.post("/student_card")
async def post_student_card(student_card: StudentsCardSh,

                            db: AsyncSession = Depends(get_db)):
    student_card = await format_card_to_dict(student_card)

    validate_personal_data(jsonable_encoder(student_card.get("personal_data")))
    validate_educational_data(jsonable_encoder(student_card.get("educational_data")))
    validate_contact_data(jsonable_encoder(student_card.get("contact_data")))
    validate_other_data(jsonable_encoder(student_card.get("other_data")))

    result = await add_commit_students_card(db, student_card)
    return result


@router.put("/change_student_card")
async def change_student_card(token: str = Depends(get_current_active_auth_user),
                              personal_id: int = None,
                              table_name: str = Query(enum=list(models_dict.keys())),
                              parameters: dict = None,
                              db: AsyncSession = Depends(get_db)):
    data = {"personal_id": personal_id,
            "table_name": table_name,
            "parameters": parameters}

    updated_data = await change_card(db, data)
    return updated_data


@router.delete("/delete_student_card")
async def delete_student_card(token: str = Depends(get_current_active_auth_user),
                              personal_id: int = None,
                              db: AsyncSession = Depends(get_db)):
    result = await delete_card(db, personal_id)
    return result
