from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.astronomy.endpoints import event
from app.contact.endpoints import contact
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSIONS)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(event.router, prefix=settings.API_V1_STR, tags=["Astronomical Events"])
app.include_router(contact.router,  prefix=settings.API_V1_STR,  tags=["Send Email"])
