import asyncio
import logging

from sqlalchemy import select

from db.database import engine, SessionLocal, Base
from schemas.benefits_data import BenefitsDataSh
from schemas.contact_data import ContactDataSh
from schemas.educational_data import EducationalDataSh
from schemas.millitary_data import MilitaryDataSh
from schemas.other_data import OtherDataSh
from schemas.personal_data import PersonalDataSh
from schemas.short_card import ShortCard
from models.educational_data import EducationalData
from models.personal_data import PersonalData
from models.contact_data import ContactData
from models.other_data import OtherData
from models.stipend_data import StipendData
from models.benefits_data import BenefitsData
from models.military_data import MilitaryData
from schemas.stipend_data import StipendDataSh
from schemas.students_card import StudentsCardSh

logging.basicConfig(filename='db_log.log', level=logging.INFO,
                    filemode="w", format="%(asctime)s %(levelname)s %(message)s")


async def get_db():
    """
    Функция инициализирует базу данных при первом
    вызове и создает новую сессию базы данных
    :return: Объект сессии
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def add_data(db, data, table):
    """
    Функция для вставки данных в талицу БД
    :param db: Объект сессии
    :param data: Данные
    :param table: Таблица
    :return: Добавленные данные
    """
    async with db.begin():
        try:
            if type(data) == dict:
                new_data = table(**data)
            else:
                new_data = table(**data.dict())

            db.add(new_data)
            await db.commit()
            await db.refresh(new_data)
            return data
        except Exception as e:
            logging.error(e)
            print(e)


async def add_students_card(db, data):
    """
    Функция для вставки личной карты студента в талицу БД
    :param db: Объект сессии
    :param data: Данные
    :return:
    """

    tables = [PersonalData, EducationalData, ContactData,
              BenefitsData, StipendData, MilitaryData, OtherData]

    data = [data.personal_data.dict(), data.educational_data.dict(),
            data.contact_data.dict(), data.benefits_data.dict(),
            data.stipend_data.dict(), data.military_data.dict(),
            data.other_data.dict()]

    for table, data in zip(tables, data):
        await add_data(db, data, table)


async def get_all_students_cards(db):
    """
    Функция для получения всех карт студентов
    :param db: Объект сессии
    :return: Все карты студентов
    """
    try:
        personal_stmt = select(PersonalData)
        educational_stmt = select(EducationalData)
        contact_stmt = select(ContactData)
        military_stmt = select(MilitaryData)
        benefits_stmt = select(BenefitsData)
        stipend_stmt = select(StipendData)
        other_stmt = select(OtherData)

        personal_results = await db.execute(personal_stmt)
        educational_results = await db.execute(educational_stmt)
        contact_results = await db.execute(contact_stmt)
        military_results = await db.execute(military_stmt)
        benefits_results = await db.execute(benefits_stmt)
        stipend_results = await db.execute(stipend_stmt)
        other_results = await db.execute(other_stmt)

        data = {"personal_data": personal_results.scalars().all(),
                "educational_data": educational_results.scalars().all(),
                "contact_data": contact_results.scalars().all(),
                "military_data": military_results.scalars().all(),
                "benefits_data": benefits_results.scalars().all(),
                "stipend_data": stipend_results.scalars().all(),
                "other_data": other_results.scalars().all()}

        return data
    except Exception as e:
        logging.error(e)


async def get_short_cards(db, filters: dict = None):
    """
    Функция для получения списка краткого представления карт студентов
    :param db: Объект сессии
    :param filters: Фильтры
    :return: Список карт студентов
    """
    try:
        faculty, direction, course, department, group, subgroup = filters.values()

        cols = [PersonalData.firstname,
                PersonalData.lastname,
                PersonalData.patronymic,
                EducationalData.direction,
                EducationalData.course,
                EducationalData.department,
                EducationalData.group,
                EducationalData.subgroup]

        stmt = select(*cols).join(EducationalData, PersonalData.id == EducationalData.personal_id)

        if faculty:
            stmt = stmt.where(EducationalData.faculty == faculty)
        if direction:
            stmt = stmt.where(EducationalData.direction == direction)
        if course:
            stmt = stmt.where(EducationalData.course == course)
        if department:
            stmt = stmt.where(EducationalData.department == department)
        if group:
            stmt = stmt.where(EducationalData.group == group)
        if subgroup:
            stmt = stmt.where(EducationalData.subgroup.in_(subgroup))

        results = await db.execute(stmt)
        data = [ShortCard.from_orm(card) for card in results.all()]
        return data
    except Exception as e:
        logging.error(e)


async def drop_table():
    async with engine.begin() as conn:
        # Удаление таблицы
        await conn.run_sync(EducationalData.metadata.drop_all)


async def main():
    await drop_table()


# asyncio.run(main())
