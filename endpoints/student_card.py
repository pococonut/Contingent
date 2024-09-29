from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from auth.validation import get_current_active_auth_user
from general.dicts import models_dict
from db.db_commands import get_db, change_card, delete_card, format_card_to_dict, add_commit_students_card
from schemas.students_card import StudentsCardSh

router = APIRouter()


@router.post("/student_card")
async def post_student_card(student_card: StudentsCardSh,
                            token: str = Depends(get_current_active_auth_user),
                            db: AsyncSession = Depends(get_db)):
    student_card = await format_card_to_dict(student_card)
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
