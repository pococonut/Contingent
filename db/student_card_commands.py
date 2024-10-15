import logging

from fastapi import HTTPException
from sqlalchemy import select, update

from general.dicts import student_card_models_dict
from models.student_card.personal_data import PersonalData


async def format_card_to_dict(s_card):
    """
    Функция для приведения данных карты студента к нужному виду
    :param s_card: Карта студента типа StudentsCardSh
    :return: Данные карты студента в виде списка словарей
    """
    return {"personal_data": s_card.personal_data.dict(),
            "educational_data": s_card.educational_data.dict(),
            "stipend_data": s_card.stipend_data.dict(),
            "contact_data": s_card.contact_data.dict(),
            "military_data": s_card.military_data.dict(),
            "benefits_data": s_card.benefits_data.dict(),
            "other_data": s_card.other_data.dict(),
            "history_data": s_card.history_data.dict(),
            "order_data": s_card.order_data.dict()}


async def add_student_data(db, student_card):
    """
    Функция для добавления личной карты студента в таблицы БД
    :param db: Объект сессии
    :param student_card: Личная карта
    :return: Объект сессии
    """
    for table_name, table in student_card_models_dict.items():
        db.add(table(**student_card.get(table_name)))
    return db


async def add_commit_students_cards(db, student_cards):
    """
    Функция для вставки личных карт студента в таблицы БД
    :param db: Объект сессии
    :param student_cards: Список личных карт
    :return: Список личных карт при успешном выполнении
    """
    try:
        for student_card in student_cards:
            db = await add_student_data(db, student_card)
        await db.commit()
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=f"Import Error.\n {e}")

    return student_cards


async def add_commit_students_card(db, student_card):
    """
    Функция для вставки личной карты студента в таблицы БД
    :param db: Объект сессии
    :param student_card: Личная карта
    :return: Личная карта студента при успешном выполнении
    """
    try:
        db = await add_student_data(db, student_card)
        await db.commit()
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=f"Import Error.\n {e}")

    return student_card


async def change_card(db, data):
    """
    Функция для изменения данных личной карточки студента
    :param db: Объект сессии
    :param data: Словарь, содержащий имя таблицы,
     параметры для изменения, идентификатор студента
    :return: Измененная карточка студента
    """
    table_name = data.get("table_name")
    parameters = data.get("parameters")
    personal_id = data.get("personal_id")

    table = student_card_models_dict.get(table_name)

    if table_name == "personal_data":
        student_id = table.id
    else:
        student_id = table.personal_id

    try:
        for parameter, new_val in parameters.items():
            stmt = update(table).where(student_id == personal_id)
            stmt = stmt.values({f"{parameter}": new_val})
            await db.execute(stmt)
        await db.commit()

        stmt = select(table).where(student_id == personal_id)
        result = await db.execute(stmt)
        updated_data = result.scalars().all()
        return updated_data

    except Exception as e:
        logging.error(e)


async def delete_card(db, p_id):
    """
    Функция для удаления личной карточки студента
    :param db: Объект сессии
    :param p_id: Идентификатор студента
    :return: Идентификатор студента при успешном выполнении
    """
    try:
        student = await db.get(PersonalData, p_id)
        await db.delete(student)
        await db.commit()
        return {"result": f"Student {p_id} was successfully deleted"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=f"Deletion Error.\n {e}")

