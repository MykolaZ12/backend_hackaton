from fastapi_mail import ConnectionConfig

from config import local_config

PROJECT_NAME = "FastAPI - Astronomical Events"
VERSIONS = 1.0

API_V1_STR = "/api/v1"

SQLALCHEMY_DATABASE_URL = local_config.SQLALCHEMY_DATABASE_URL

SECRET_KEY = local_config.SECRET_KEY

BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

conf = ConnectionConfig(
    MAIL_USERNAME=local_config.MAIL_USERNAME,
    MAIL_PASSWORD=local_config.MAIL_PASSWORD,
    MAIL_FROM=local_config.MAIL_FROM,
    MAIL_PORT=local_config.MAIL_PORT,
    MAIL_SERVER=local_config.MAIL_SERVER,
    MAIL_FROM_NAME=local_config.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False
)
