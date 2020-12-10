from fastapi import APIRouter, Depends
from examples.schema import EmailSchema
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from config.settings import conf
from app.contact import services, schemas
from db.db import get_db

router = APIRouter()


@router.post("/email")
async def send_in_background(
        background_tasks: BackgroundTasks,
        email: schemas.EmailSchema,
        db: Session = Depends(get_db)
) -> JSONResponse:
    message = MessageSchema(
        subject="Підписка на розсилку",
        recipients=[email.email],
        body="Дякуєм вам, що ви підписались на розсилку про астрономічні події",
    )

    fm = FastMail(conf)
    if not services.get_by_email(db=db, email=email.email):
        services.create(db=db, schema=schemas.ContactCreate(email=email.email))
    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
