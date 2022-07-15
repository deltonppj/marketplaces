import os

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'

    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_db: str = os.getenv("POSTGRES_DB")

    DB_URL: str = f'postgresql+asyncpg://{postgres_user}:{postgres_password}@localhost:5432/{postgres_db}'
    DBBaseModel: declarative_base = declarative_base()

    JWT_SECRET_KEY: str = os.getenv('SECRET_KEY')
    '''
    import secrets
    secrets.token_urlsafe(32)
    '''
    ALGORITHM: str = 'HS256'

    # 60 minutos * 24 horas * 365 dias => 1 ano
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 365

    class Config:
        case_sensitive = True


settings = Settings()
