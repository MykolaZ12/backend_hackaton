from fastapi import FastAPI
from app.astronomy.endpoints import event
from app.contact.endpoints import contact


app = FastAPI()

app.include_router(event.router, prefix="/event", tags=["Astronomical Events"])
app.include_router(contact.router, tags=["Send Email"])
