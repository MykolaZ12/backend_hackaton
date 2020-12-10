from sqlalchemy import Column, Integer, DateTime, String

from db.db import Base


class AstronomicalEvents(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    day = Column(DateTime)
    event_ua = Column(String)
    event_en = Column(String)