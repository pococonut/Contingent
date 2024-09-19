import jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, Query, UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_KEY, ALGORITHM
from auth.authentication import fake_users_db, create_access_token, verify_password, get_current_user
from general.dicts import models_dict
from general.excel_functions import read_excel_file, get_cards_form_df
from general.number_contingent import get_students_number_contingent
from schemas.authentication import User, UserOut
from schemas.students_card import StudentsCardSh
from db.db_commands import get_db, get_filtered_cards, add_commit_students_card, change_card, delete_card, \
    add_commit_students_cards, format_card_to_dict


app = FastAPI(title="Contingent")


@app.post('/login')
async def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(from_data.username, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user['password']

    if not verify_password(from_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {"access_token": create_access_token(user['username'])}


@app.get('/refresh')
async def refresh(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    user = fake_users_db[username]

    return {"access_token": create_access_token(user['username'])}


@app.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: str = Depends(get_current_user)):
    return user


@app.get('/students_cards')
async def get_students_cards(user: Annotated[User, Depends(get_current_user)],
                             firstname: Annotated[str | None, Query()] = None,
                             lastname: Annotated[str | None, Query()] = None,
                             faculty: Annotated[str | None, Query()] = None,
                             direction: Annotated[str | None, Query()] = None,
                             course: Annotated[str | None, Query()] = None,
                             department: Annotated[str | None, Query()] = None,
                             group: Annotated[str | None, Query()] = None,
                             subgroup: Annotated[str | None, Query()] = None,
                             session: AsyncSession = Depends(get_db)):
    filters = {"personal_filters": {"firstname": firstname,
                                    "lastname": lastname},

               "educational_filters": {"faculty": faculty,
                                       "direction": direction,
                                       "course": course,
                                       "department": department,
                                       "group": group,
                                       "subgroup": subgroup}}

    students_cards = await get_filtered_cards(session, filters)
    return students_cards


@app.get("/number_contingent")
async def get_number_contingent(user: Annotated[User, Depends(get_current_user)],
                                firstname: Annotated[str | None, Query()] = None,
                                lastname: Annotated[str | None, Query()] = None,
                                faculty: Annotated[str | None, Query()] = None,
                                direction: Annotated[str | None, Query()] = None,
                                course: Annotated[str | None, Query()] = None,
                                department: Annotated[str | None, Query()] = None,
                                group: Annotated[str | None, Query()] = None,
                                subgroup: Annotated[str | None, Query()] = None,
                                session: AsyncSession = Depends(get_db),

                                ):
    filters = {"personal_filters": {"firstname": firstname,
                                    "lastname": lastname},

               "educational_filters": {"faculty": faculty,
                                       "direction": direction,
                                       "course": course,
                                       "department": department,
                                       "group": group,
                                       "subgroup": subgroup}}
    students_cards = await get_filtered_cards(session, filters)
    number_contingent = await get_students_number_contingent(students_cards)
    return number_contingent


@app.get("/table_data")
async def get_table_data(user: Annotated[User, Depends(get_current_user)],
                         table_name: str = Query(enum=list(models_dict.keys())),
                         db: AsyncSession = Depends(get_db)):
    table = models_dict.get(table_name)
    result = await db.execute(select(table))
    data = result.scalars().all()
    return {f"{table_name}": data}


@app.post("/student_card")
async def post_student_card(user: Annotated[User, Depends(get_current_user)],
                            student_card: StudentsCardSh,
                            db: AsyncSession = Depends(get_db)):
    student_card = await format_card_to_dict(student_card)
    result = await add_commit_students_card(db, student_card)
    return result


@app.post("/import_cards_excel")
async def import_cards_excel(user: Annotated[User, Depends(get_current_user)],
                             file: UploadFile, db: AsyncSession = Depends(get_db)):
    file = await file.read()
    df = await read_excel_file(file)
    student_cards = await get_cards_form_df(df)
    response = await add_commit_students_cards(db, student_cards)
    return response


@app.put("/change_student_card")
async def change_student_card(user: Annotated[User, Depends(get_current_user)],
                              personal_id: int,
                              table_name: str = Query(enum=list(models_dict.keys())),
                              parameters: dict = None,
                              db: AsyncSession = Depends(get_db)):
    data = {"personal_id": personal_id,
            "table_name": table_name,
            "parameters": parameters}

    updated_data = await change_card(db, data)
    return updated_data


@app.delete("/delete_student_card")
async def delete_student_card(user: Annotated[User, Depends(get_current_user)],
                              personal_id: int,
                              db: AsyncSession = Depends(get_db)):
    result = await delete_card(db, personal_id)
    return result
