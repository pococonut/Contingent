from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import DB_URL


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DB_URL, echo=False)
SessionLocal = async_sessionmaker(engine)

