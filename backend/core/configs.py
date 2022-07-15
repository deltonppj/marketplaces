import os

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://drakon:mudar123@localhost:5432/marketplaces'
    DBBaseModel: declarative_base = declarative_base()

    JWT_SECRET_KEY: str = os.getenv('SECRET_KEY')
    '''
    import secrets
    secrets.token_urlsafe(32)
    '''
    ALGORITHM: str = 'HS256'

    # 60 minutos * 24 horas * 365 dias => 1 ano
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    class Config:
        case_sensitive = True


settings = Settings()
