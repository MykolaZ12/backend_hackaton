from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    day: date
    event_ua: str
    event_en: str

    class Config:
        orm_mode = True


class EventGet(EventBase):
    id: int
    day: datetime
    cloud: Optional[int] = None


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass
