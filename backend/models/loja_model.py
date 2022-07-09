from core.configs import settings

from sqlalchemy import Column, Integer, String


class LojaModel(settings.DBBaseModel):
    __tablename__: str = 'lojas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False, unique=True)
