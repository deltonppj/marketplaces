from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.configs import settings


class LojaModel(settings.DBBaseModel):
    __tablename__: str = 'lojas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False, unique=True)

    produtos = relationship(
        'ProdutoModel',
        cascade='all, delete-orphan',
        back_populates='loja_model',
        uselist=True,
        lazy='subquery')

    ppms = relationship('LojaProgramaPontos', back_populates='loja', uselist=True, lazy='subquery')
    vendas = relationship('VendaModel', back_populates='lojas', uselist=True, lazy='subquery')