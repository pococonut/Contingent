from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from auth.validation import get_current_active_auth_user
from general.excel_functions import read_excel_file, get_cards_form_df
from db.db_commands import get_db, add_commit_students_cards


router = APIRouter()


@router.post("/import_cards_excel")
async def import_cards_excel(file: UploadFile,
                             db: AsyncSession = Depends(get_db)):
    file = await file.read()
    df = await read_excel_file(file)
    student_cards = await get_cards_form_df(df)
    response = await add_commit_students_cards(db, student_cards)
    return response

