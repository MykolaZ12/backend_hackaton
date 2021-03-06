from typing import List

from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.contact.models import Contact
from app.contact.schemas import ContactCreate


def get_contact(db: Session, id: int) -> Contact:
    contact = db.query(Contact).filter(Contact.id == id).first()
    return contact


def get_multi_contact(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Contact]:
    return db.query(self.model).offset(skip).limit(limit).all()


def get_contact_by_email(db: Session, email: EmailStr) -> Contact:
    contact = db.query(Contact).filter(Contact.email == email).first()
    return contact


def create_contact(db: Session, *, schema: ContactCreate) -> Contact:
    """Add email contact in database"""
    obj_in_data = jsonable_encoder(schema)
    db_obj = Contact(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
