from typing import Optional, List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.astronomy.models import AstronomicalEvents
from app.astronomy.schemas import EventCreate, EventUpdate


def get(db: Session, id: int) -> Optional[AstronomicalEvents]:
    return db.query(AstronomicalEvents).filter(AstronomicalEvents == id).first()


def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[AstronomicalEvents]:
    return db.query(AstronomicalEvents).offset(skip).limit(limit).all()


def create(db: Session, *, schema: EventCreate) -> AstronomicalEvents:
    obj_in_data = jsonable_encoder(schema)
    db_obj = AstronomicalEvents(**obj_in_data)  # type: ignore
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="IntegrityError")
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
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="IntegrityError")
    return db_obj


def remove(db: Session, *, id: int) -> AstronomicalEvents:
    obj = db.query(AstronomicalEvents).get(id)
    db.delete(obj)
    db.commit()
    return obj
