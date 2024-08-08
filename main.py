from io import BytesIO

import pandas as pd
from fastapi import FastAPI, Depends, Query, UploadFile
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.educational_data import EducationalData
from models.personal_data import PersonalData
from models.contact_data import ContactData
from models.other_data import OtherData
from models.stipend_data import StipendData
from models.benefits_data import BenefitsData
from models.military_data import MilitaryData
from schemas.educational_data import EducationalDataSh
from schemas.personal_data import PersonalDataSh
from schemas.students_card import StudentsCardSh
from db.db_commands import get_db, add_data, get_short_cards, add_students_card, get_all_students_cards


app = FastAPI(title="Contingent")


@app.post("/students_card")
async def post_students_card(students_card: StudentsCardSh, db: AsyncSession = Depends(get_db)):
    await add_students_card(db, students_card)
    return students_card


@app.get("/students_card")
async def get_students_card(db: AsyncSession = Depends(get_db)):
    res = await get_all_students_cards(db)
    return res


@app.post("/personal_data")
async def post_personal_data(personal_data: PersonalDataSh,
                             db: AsyncSession = Depends(get_db)):
    result = await add_data(db, personal_data, PersonalData)
    return result


@app.get("/personal_data")
async def get_personal_data(db: AsyncSession = Depends(get_db)):
    results = await db.execute((select(PersonalData)))
    data = results.scalars().all()
    return {"personal_data_of_students": data}


@app.post("/educational_data")
async def post_educational_data(educational_data: EducationalDataSh,
                                db: AsyncSession = Depends(get_db)):
    result = await add_data(db, educational_data, EducationalData)
    return result


@app.get("/educational_data")
async def get_educational_data(db: AsyncSession = Depends(get_db)):
    results = await db.execute((select(EducationalData)))
    data = results.scalars().all()
    return {"educational_data_of_students": data}


@app.get('/short_cards')
async def get_short_cards(faculty: Annotated[str | None, Query(example='МИКН')] = None,
                          direction: Annotated[str | None, Query(example='ФМИМ')] = None,
                          course: Annotated[str | None, Query(example='2')] = None,
                          department: Annotated[str | None, Query(example='ВМИ')] = None,
                          group: Annotated[str | None, Query(example='21')] = None,
                          subgroup: Annotated[list[str] | None, Query(example='21/2')] = None,
                          session: AsyncSession = Depends(get_db)):
    filters = {"faculty": faculty,
               "direction": direction,
               "course": course,
               "department": department,
               "group": group,
               "subgroup": subgroup, }

    short_cards = await get_short_cards(session, filters)
    return short_cards


@app.post("/import_cards_excel")
async def import_cards_excel(file: UploadFile, db: AsyncSession = Depends(get_db)):
    data = await file.read()
    excel_data = BytesIO(data)
    df = pd.read_excel(excel_data, header=1)
    amount_rows = df.shape[0]

    for i in range(int(amount_rows)):
        personal_data = {"id": i,
                         "firstname": df.at[i, 'Имя'],
                         "lastname": df.at[i, 'Фамилия'],
                         "patronymic": df.at[i, 'Отчество'],
                         "birth_date": df.at[i, 'Дата рожд.'],
                         "birth_place": "",
                         "citizenship": df.at[i, 'Гражданство'],
                         "type_of_identity": df.at[i, 'Удостов. личности'],
                         "address": df.at[i, 'Адрес'],
                         "marital_status": "",
                         "snils": str(df.at[i, 'Снилс']),
                         "polis": "",
                         "study_status": df.at[i, 'Статус внутри вуза'],
                         "general_status": df.at[i, 'Статус общий'], }

        educational_data = {"faculty": df.at[i, 'Факультет'],
                            "direction": df.at[i, 'Направление'],
                            "course": str(df.at[i, 'Курс']),
                            "department": "",
                            "group": str(df.at[i, 'Группа']),
                            "subgroup": df.at[i, 'Подгруппа'],
                            "form": "",
                            "book_num": str(df.at[i, 'Номер зачётки']),
                            "degree": df.at[i, 'Степень обучения'],
                            "degree_payment": df.at[i, 'Форма обуч. $'],
                            "personal_id": i, }

        contact_data = {"number": str(df.at[i, 'Тел.']),
                        "spare_number": str(df.at[i, '2й Тел.']),
                        "mail": str(df.at[i, 'Почта']),
                        "personal_id": i}

        benefit_data = {"benefits": str(df.at[i, 'Льготы']),
                        "personal_id": i}

        stipend_data = {"form": str(df.at[i, 'Форма']),
                        "amount": str(df.at[i, 'Сумма']),
                        "personal_id": i, }

        military_data = {"status": str(df.at[i, 'Статус']),
                         "category": str(df.at[i, 'Категория']),
                         "delay": str(df.at[i, 'Отсрочка']),
                         "document": str(df.at[i, 'Документ']),
                         "personal_id": i, }

        other_data = {"parents": str(df.at[i, 'Родители']),
                      "parents_contacts": str(df.at[i, 'Контакты родственников']),
                      "relatives_works": str(df.at[i, 'Места работы родственников']),
                      "relatives_addresses": str(df.at[i, 'Адреса родственников']),
                      "personal_id": i, }

        await add_data(db, personal_data, PersonalData)
        await add_data(db, educational_data, EducationalData)
        await add_data(db, contact_data, ContactData)
        await add_data(db, benefit_data, BenefitsData)
        await add_data(db, stipend_data, StipendData)
        await add_data(db, military_data, MilitaryData)
        await add_data(db, other_data, OtherData)

    return {"file": file.filename}
