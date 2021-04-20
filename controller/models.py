from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)

    datetime = Column(DateTime)
    status = Column(String(4))
