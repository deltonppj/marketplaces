from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://drakon:mudar123@localhost:5432/marketplaces'
    DBBaseModel: declarative_base = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
