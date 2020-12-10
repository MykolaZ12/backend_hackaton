from sqlalchemy import Column, Integer, DateTime, String, Boolean

from db.db import Base


class AstronomicalEvents(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    event_ua = Column(String)
    event_en = Column(String)
    img = Column(String(50))
    active = Column(Boolean, default=True)