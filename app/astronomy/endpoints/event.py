from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db import get_db
from app.astronomy import schemas, services, models

router = APIRouter()


@router.get("/event/{id}", response_model=schemas.EventGet)
def get_event(id: int, city: str, db: Session = Depends(get_db)):
    """Get one astronomical event"""
    event = services.get_event(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event = services.add_field_cloud_percent(city=city, event_obj=[event])
    setattr(event[0], "duration", str(event[0].date_end - event[0].date_start))
    return event[0]


@router.get("/event/", response_model=List[schemas.EventGet])
def filter_events(*, day_from: str = "2020-12-01", day_to: str = "2020-12-31", city: str,
                  db: Session = Depends(get_db)):
    """Filter astronomical event, return list events"""
    events = services.filter_event_by_date(db=db, day_from=day_from, day_to=day_to)
    if not events:
        raise HTTPException(status_code=404, detail="Events not found")
    events = services.add_field_cloud_percent(city=city, event_obj=events)
    return events


@router.post("/event/", response_model=schemas.EventCreate)
def create_event(*, db: Session = Depends(get_db), schema: schemas.EventCreate):
    """Add to database astronomical events"""
    return services.create_event(db=db, schema=schema)


@router.put("/event/{id}", response_model=schemas.EventUpdate)
def update_event(*, id: int, db: Session = Depends(get_db), schema: schemas.EventUpdate):
    """Update in database astronomical event"""
    event = services.get_event(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = services.update(db=db, schema=schema, db_obj=event)
    return event


@router.delete("/event/{id}", response_model=schemas.EventGet)
def delete_event(id: int, db: Session = Depends(get_db)):
    """Delete in n database astronomical event"""
    event = services.get_event(db=db, id=id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return services.remove(db=db, id=id)
