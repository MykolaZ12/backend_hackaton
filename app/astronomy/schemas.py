from datetime import datetime, date

from pydantic import BaseModel


class EventBase(BaseModel):
    day: date
    event: str

    class Config:
        orm_mode = True


class EventGet(EventBase):
    id: int


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass
