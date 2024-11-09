from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db
from db.student_card_commands import add_commit_students_cards
from helpers.excel_functions import read_excel_file, get_cards_form_df
from validation.auth_parameters import get_current_active_auth_user

router = APIRouter()


@router.post("/import_cards_excel",
             tags=['excel'],
             response_description="Карточки студентов")
async def import_cards_excel(file: UploadFile,
                             token: str = Depends(get_current_active_auth_user),
                             db: AsyncSession = Depends(get_db)):
    """
    Импортирует Карточки студентов из exel-файла в базу данных
    - file: Exel-файл с картами студентов
    """
    file = await file.read()
    df = await read_excel_file(file)
    student_cards = await get_cards_form_df(df)
    response = await add_commit_students_cards(db, student_cards)
    return response

