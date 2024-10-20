from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db
from db.student_card_commands import add_commit_students_cards
from helpers.excel_functions import read_excel_file, get_cards_form_df


router = APIRouter()


@router.post("/import_cards_excel", tags=['excel'])
async def import_cards_excel(file: UploadFile,
                             db: AsyncSession = Depends(get_db)):
    file = await file.read()
    df = await read_excel_file(file)
    student_cards = await get_cards_form_df(df)
    response = await add_commit_students_cards(db, student_cards)
    return response

