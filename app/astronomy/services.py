import json
import re
from typing import Optional, List

import requests
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.astronomy.models import AstronomicalEvents
from app.astronomy.schemas import EventCreate, EventUpdate


def get_weather_in_city(city: str, day: int) -> List[list]:
    """Returns a list of weather by hours of each day"""
    r = requests.get(
        f'http://api.weatherapi.com/v1/forecast.json?key=bf244d3c98364dcdae8193835200912&q={city}&days={day}')
    data = json.loads(r.content)
    lst_hour = []
    for el in data["forecast"]["forecastday"]:
        lst_hour.append(el["hour"])
    print(len(lst_hour))
    return lst_hour


def add_field_cloud_percent(
        *,
        city: str,
        hour: str,
        day: int = 10,
        event_obj: List[AstronomicalEvents]
) -> List[AstronomicalEvents]:
    """
    Creates an additional cloud  field for each object in the list[AstronomicalEvents]
    If information is available cloud = percentage of clouds
    """
    data = get_weather_in_city(city=city, day=day)
    for obj in event_obj:
        event_day = re.split(" ", str(obj.day))[0]
        for day in data:
            for el in day:
                if re.split(" ", el["time"])[0] == event_day:
                    if re.split(" ", el["time"])[-1] == hour:
                        setattr(obj, "cloud", el["cloud"])
    return event_obj


def get_event(db: Session, id: int) -> AstronomicalEvents:
    event = db.query(AstronomicalEvents).filter(AstronomicalEvents.id == id).first()
    return event


def filter_event_by_date(db: Session, *, day_from: str, day_to: str) -> List[AstronomicalEvents]:
    return db.query(AstronomicalEvents).filter(
        AstronomicalEvents.day.between(day_from, day_to)).all()


def create_event(db: Session, *, schema: EventCreate) -> AstronomicalEvents:
    obj_in_data = jsonable_encoder(schema)
    db_obj = AstronomicalEvents(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(*, db: Session, db_obj: AstronomicalEvents, schema: EventUpdate) -> AstronomicalEvents:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(schema, dict):
        update_data = schema
    else:
        update_data = schema.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, *, id: int) -> AstronomicalEvents:
    obj = db.query(AstronomicalEvents).get(id)
    db.delete(obj)
    db.commit()
    return obj
