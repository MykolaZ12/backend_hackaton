from fastapi_mail import ConnectionConfig

from config import local_config

SQLALCHEMY_DATABASE_URL = "postgresql://admin:password1234@tymkiv.pp.ua:5432/postgres"

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
