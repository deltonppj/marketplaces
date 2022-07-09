from core.settings import settings

from sqlalchemy import Column, Integer, String


class LojaModel(settings.DBBaseModel):
    __tablename__ = 'lojas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
