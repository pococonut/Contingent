from io import BytesIO
from collections import defaultdict, Counter

import pandas as pd
from fastapi import FastAPI, Depends, Query, UploadFile
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from general.dicts import models_dict
from schemas.students_card import StudentsCardSh
from db.db_commands import get_db, get_filtered_cards, add_students_card

app = FastAPI(title="Contingent")


@app.get('/students_cards')
async def get_students_cards(faculty: Annotated[str | None, Query()] = None,
                             direction: Annotated[str | None, Query()] = None,
                             course: Annotated[str | None, Query()] = None,
                             department: Annotated[str | None, Query()] = None,
                             group: Annotated[str | None, Query()] = None,
                             subgroup: Annotated[list[str] | None, Query()] = None,
                             session: AsyncSession = Depends(get_db)):
    filters = [faculty, direction, course, department, group, subgroup]

    students_cards = await get_filtered_cards(session, filters)
    return students_cards


@app.get("/number_contingent")
async def get_number_contingent(faculty: Annotated[str | None, Query()] = None,
                                direction: Annotated[str | None, Query()] = None,
                                course: Annotated[str | None, Query()] = None,
                                department: Annotated[str | None, Query()] = None,
                                group: Annotated[str | None, Query()] = None,
                                subgroup: Annotated[list[str] | None, Query()] = None,
                                session: AsyncSession = Depends(get_db)):
    filters = [faculty, direction, course, department, group, subgroup]
    students_cards = await get_filtered_cards(session, filters)

    subgroups_lists = defaultdict(list)
    degree_payment_lists = defaultdict(list)
    for k, v in students_cards.items():
        subgroups_lists[v.get("group")].append(v.get("subgroup"))
        degree_payment_lists[v.get("group")].append(v.get("degree_payment"))

    group_students_amount = defaultdict()
    degree_students_amount = defaultdict()
    total_students_amount = defaultdict(dict)
    for k, v in subgroups_lists.items():
        group_students_amount[k] = Counter(v)
    for k, v in subgroups_lists.items():
        total_students_amount[k] = {"total": len(v)}
    for k, v in degree_payment_lists.items():
        degree_students_amount[k] = Counter(v)

    number_contingent = defaultdict()
    for k in group_students_amount:
        number_contingent[k] = group_students_amount[k].copy()
    for k in number_contingent:
        number_contingent[k].update(degree_students_amount[k])
        number_contingent[k].update(total_students_amount[k])

    return number_contingent


@app.get("/table_data")
async def get_personal_data(table_name: str = Query(enum=list(models_dict.keys())),
                            db: AsyncSession = Depends(get_db)):
    table = models_dict.get(table_name)
    result = await db.execute(select(table))
    data = result.scalars().all()
    return {f"{table_name}": data}


@app.post("/students_card")
async def post_students_card(students_card: StudentsCardSh,
                             db: AsyncSession = Depends(get_db)):
    result = await add_students_card(db, students_card)
    return result


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
                         "birth_place": df.at[i, 'Место рожд.'],
                         "citizenship": df.at[i, 'Гражданство'],
                         "type_of_identity": df.at[i, 'Удостов. личности'],
                         "address": df.at[i, 'Адрес'],
                         "snils": str(df.at[i, 'Снилс']),
                         "polis": str(df.at[i, 'Полис']),
                         "study_status": df.at[i, 'Статус внутри вуза'],
                         "general_status": df.at[i, 'Статус общий'],
                         "gender": df.at[i, 'Пол']}

        educational_data = {"faculty": df.at[i, 'Факультет'],
                            "direction": df.at[i, 'Направление'],
                            "course": str(df.at[i, 'Курс']),
                            "department": str(df.at[i, 'Кафедра']),
                            "group": str(df.at[i, 'Группа']),
                            "subgroup": df.at[i, 'Подгруппа'],
                            "book_num": str(df.at[i, 'Номер зачётки']),
                            "form": str(df.at[i, 'Форма обуч.']),
                            "degree": df.at[i, 'Степень обуч.'],
                            "degree_payment": df.at[i, 'Форма обуч. $'],
                            "study_duration": str(df.at[i, 'Период обуч.']),
                            "study_duration_total": str(df.at[i, 'Срок обуч.']),
                            "study_profile": str(df.at[i, 'Профиль обуч.']),
                            "current_year": str(df.at[i, 'Текущий год обуч.']),
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

        history_data = {"movements": str(df.at[i, 'История перемещений (курс)']),
                        "statuses": str(df.at[i, 'История статусов']),
                        "personal_id": i, }

        order_data = {"order": str(df.at[i, 'Приказы']),
                      "personal_id": i, }

        student_card = [personal_data, educational_data, stipend_data, contact_data,
                        military_data, benefit_data, other_data, history_data, order_data]

        await add_students_card(db, student_card)

    return {"file": file.filename}
