from collections import defaultdict, Counter

from fastapi import FastAPI, Depends, Query, UploadFile
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from general.dicts import models_dict
from general.excel_functions import parse_excel_row, read_excel_file
from schemas.students_card import StudentsCardSh
from db.db_commands import get_db, get_filtered_cards, add_commit_students_card, change_card, delete_card, \
    add_commit_students_cards, format_card_to_dict

app = FastAPI(title="Contingent")


@app.get('/students_cards')
async def get_students_cards(firstname: Annotated[str | None, Query()] = None,
                             lastname: Annotated[str | None, Query()] = None,
                             faculty: Annotated[str | None, Query()] = None,
                             direction: Annotated[str | None, Query()] = None,
                             course: Annotated[str | None, Query()] = None,
                             department: Annotated[str | None, Query()] = None,
                             group: Annotated[str | None, Query()] = None,
                             subgroup: Annotated[list[str] | None, Query()] = None,
                             session: AsyncSession = Depends(get_db)):
    filters = {"personal_filters": [firstname, lastname],
               "educational_filters": [faculty, direction, course, department, group, subgroup]}

    students_cards = await get_filtered_cards(session, filters)
    return students_cards


@app.get("/number_contingent")
async def get_number_contingent(firstname: Annotated[str | None, Query()] = None,
                                lastname: Annotated[str | None, Query()] = None,
                                faculty: Annotated[str | None, Query()] = None,
                                direction: Annotated[str | None, Query()] = None,
                                course: Annotated[str | None, Query()] = None,
                                department: Annotated[str | None, Query()] = None,
                                group: Annotated[str | None, Query()] = None,
                                subgroup: Annotated[list[str] | None, Query()] = None,
                                session: AsyncSession = Depends(get_db)):
    filters = {"personal_filters": [firstname, lastname],
               "educational_filters": [faculty, direction, course, department, group, subgroup]}
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
async def get_table_data(table_name: str = Query(enum=list(models_dict.keys())),
                         db: AsyncSession = Depends(get_db)):
    table = models_dict.get(table_name)
    result = await db.execute(select(table))
    data = result.scalars().all()
    return {f"{table_name}": data}


@app.post("/student_card")
async def post_student_card(student_card: StudentsCardSh,
                            db: AsyncSession = Depends(get_db)):
    student_card = await format_card_to_dict(student_card)
    result = await add_commit_students_card(db, student_card)
    return result


@app.post("/import_cards_excel")
async def import_cards_excel(file: UploadFile, db: AsyncSession = Depends(get_db)):
    file = await file.read()
    df = await read_excel_file(file)
    amount_rows = int(df.shape[0])
    student_cards = []

    for i in range(amount_rows):
        card = await parse_excel_row(i, df)
        student_cards.append(card)

    response = await add_commit_students_cards(db, student_cards)
    return response


@app.put("/change_student_card")
async def change_student_card(personal_id: int,
                              table_name: str = Query(enum=list(models_dict.keys())),
                              parameters: dict = None,
                              db: AsyncSession = Depends(get_db)):
    data = {"personal_id": personal_id,
            "table_name": table_name,
            "parameters": parameters}

    updated_data = await change_card(db, data)
    return updated_data


@app.delete("/delete_student_card")
async def delete_student_card(personal_id: int,
                              db: AsyncSession = Depends(get_db)):
    result = await delete_card(db, personal_id)
    return result
