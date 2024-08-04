from typing import Annotated

from fastapi import FastAPI, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_commands import get_db, add_data, get_cards
from models.educational_data import EducationalData
from models.personal_data import PersonalData


app = FastAPI()


@app.post("/personal_data")
async def post_personal_data(firstname: Annotated[str | None, Query(example='Владимир')] = None,
                             lastname: Annotated[str | None, Query(example='Высоцкий')] = None,
                             patronymic: Annotated[str | None, Query(example='Семёнович')] = None,
                             db: AsyncSession = Depends(get_db)):
    data = {"firstname": firstname,
            "lastname": lastname,
            "patronymic": patronymic, }

    result = await add_data(db, data, PersonalData)
    return result


@app.get("/personal_data")
async def get_personal_data(db: AsyncSession = Depends(get_db)):
    results = await db.execute((select(PersonalData)))
    users = results.scalars().all()
    return {"personal_data_of_students": users}


@app.post("/educational_data")
async def post_educational_data(personal_id: Annotated[int, Query()],
                                faculty: Annotated[str | None, Query(example='МИКН')] = None,
                                direction: Annotated[str | None, Query(example='МИКН')] = None,
                                course: Annotated[str | None, Query(example='2')] = None,
                                department: Annotated[str | None, Query(example='ВМИ')] = None,
                                group: Annotated[str | None, Query(example='21')] = None,
                                subgroup: Annotated[str | None, Query(example='21/2')] = None,
                                db: AsyncSession = Depends(get_db)):
    data = {"personal_id": personal_id,
            "faculty": faculty,
            "direction": direction,
            "course": course,
            "department": department,
            "group": group,
            "subgroup": subgroup, }

    result = await add_data(db, data, EducationalData)
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

    short_cards = await get_cards(session, filters)
    return short_cards
