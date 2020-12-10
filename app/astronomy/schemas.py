from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    date_start: datetime
    date_end: datetime
    event_ua: str
    event_en: str

    class Config:
        orm_mode = True


class EventGet(EventBase):
    id: int
    cloud: Optional[int] = None
    duration: str


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass
