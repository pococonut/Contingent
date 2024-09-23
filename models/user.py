from sqlalchemy import Column, Integer, String

from db.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)

