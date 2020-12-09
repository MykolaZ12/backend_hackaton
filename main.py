from fastapi import FastAPI
from app.astronomy.api import router

app = FastAPI()

app.include_router(router, prefix="/event", tags=["Astronomical Events"])
