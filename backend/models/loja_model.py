from core.configs import settings

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class LojaModel(settings.DBBaseModel):
    __tablename__: str = 'lojas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False, unique=True)
    produtos = relationship(
        'ProdutoModel',
        cascade='all, delete-orphan',
        back_populates='loja_model',
        uselist=True,
        lazy='joined')
