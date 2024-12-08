import io

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db
from db.student_card_commands import add_commit_students_cards
from helpers.excel_functions import read_excel_file, get_cards_form_df
from starlette.responses import StreamingResponse

router = APIRouter()


@router.post("/import_cards_excel",
             tags=['excel'],
             response_description="Карточки студентов")
async def import_cards_excel(file: UploadFile,
                             db: AsyncSession = Depends(get_db)):
    """
    Импортирует Карточки студентов из exel-файла в базу данных
    - file: Exel-файл с картами студентов
    """
    file = await file.read()
    if len(file) >= 10485760:
        raise HTTPException(status_code=400, detail=f"Your file is more than 10MB")

    df = await read_excel_file(file)
    student_cards = await get_cards_form_df(df)
    response = await add_commit_students_cards(db, student_cards)
    return response


@router.get("/cards_excel_example",
            tags=["excel"],
            response_description="Шаблон excel файла для импорта Студенческих карт")
async def get_excel_example():
    """
    Используется для получения шаблона excel файла для импорта Студенческих карт
    """
    headers = {'Content-Disposition': 'attachment; filename="Example.xlsx"'}
    path = "./helpers/files/Example.xlsx"
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    with open(path, "rb") as file:
        bytes_file = io.BytesIO(file.read())
    return StreamingResponse(
        bytes_file,
        headers=headers,
        media_type=media_type
    )
