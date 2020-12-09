import re

import requests
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db import get_db
from app.astronomy import schemas, services, models

router = APIRouter()


@router.get("/{id}", response_model=schemas.EventGet)
def get_event(id: int, city: str, hour: str, db: Session = Depends(get_db)):
    event = services.get(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event = services.add_field_cloud_percent(city=city, hour=hour, event_obj=[event])
    return event[0]


@router.get("/", response_model=List[schemas.EventGet])
def filter_events(*, day_from: str, day_to: str, city: str, hour: str, day: int = 1,
                  db: Session = Depends(get_db)):
    events = services.filter_by_date(db=db, day_from=day_from, day_to=day_to)
    if not events:
        raise HTTPException(status_code=404, detail="Events not found")

    events = services.add_field_cloud_percent(city=city, hour=hour, day=day, event_obj=events)
    return events


@router.post("/", response_model=schemas.EventCreate)
def create_event(*, db: Session = Depends(get_db), schema: schemas.EventCreate):
    return services.create(db=db, schema=schema)


@router.put("/{id}", response_model=schemas.EventUpdate)
def update_event(*, id: int, db: Session = Depends(get_db), schema: schemas.EventUpdate):
    event = services.get(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = services.update(db=db, schema=schema, db_obj=event)
    return event


@router.delete("/{id}", response_model=schemas.EventGet)
def delete_event(id: int, db: Session = Depends(get_db)):
    event = services.get(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return services.remove(db=db, id=id)
