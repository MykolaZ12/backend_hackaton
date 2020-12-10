import json
import re
from typing import Optional, List

import requests
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.astronomy.models import AstronomicalEvents
from app.astronomy.schemas import EventCreate, EventUpdate


def get_weather_in_city(city: str) -> List[list]:
    """Returns a list of weather by hours of each day"""
    r = requests.get(
        f'https://api.weatherbit.io/v2.0/forecast/daily?city={city}&country=UA&days=16&key=59bccc40c9a94e20bc18549c20f5cb8f')
    data = json.loads(r.content)
    return data["data"]


def add_field_cloud_percent(
        *,
        city: str,
        event_obj: List[AstronomicalEvents]
) -> List[AstronomicalEvents]:
    """
    Creates an additional cloud  field for each object in the list[AstronomicalEvents]
    If information is available cloud = percentage of clouds
    """
    data = get_weather_in_city(city=city)
    for obj in event_obj:
        event_day = re.split(" ", str(obj.date_start))[0]
        setattr(obj, "duration", str(obj.date_end - obj.date_start))
        for day in data:
            if day["valid_date"] == event_day:
                setattr(obj, "cloud", day["clouds"])
    return event_obj


def get_event(db: Session, id: int) -> AstronomicalEvents:
    event = db.query(AstronomicalEvents).filter(AstronomicalEvents.id == id).filter(
        AstronomicalEvents.active.is_(True)).first()
    return event


def filter_event_by_date(db: Session, *, day_from: str, day_to: str) -> List[AstronomicalEvents]:
    return db.query(AstronomicalEvents).filter(
        AstronomicalEvents.date_start.between(day_from, day_to)).filter(
        AstronomicalEvents.active.is_(True)).all()


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
