import logging

from sqlalchemy import select

from db.database import engine, SessionLocal, Base
from schemas.short_card import ShortCard
from models.educational_data import EducationalData
from models.personal_data import PersonalData
from models.contact_data import ContactData
from models.other_data import OtherData
from models.stipend_data import StipendData
from models.benefits_data import BenefitsData
from models.military_data import MilitaryData


logging.basicConfig(filename='db/db_log.log', level=logging.INFO,
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
    try:
        new_data = table(**data)
        db.add(new_data)
        await db.commit()
        await db.refresh(new_data)
        return new_data
    except Exception as e:
        logging.error(e)
        print(e)


async def get_cards(db, filters: dict = None):
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

        stmt = select(*cols).join(EducationalData, PersonalData.personal_id == EducationalData.personal_id)

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

