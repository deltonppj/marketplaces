from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from core.configs import settings


class VendaModel(settings.DBBaseModel):
    __tablename__: str = 'vendas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    preco_venda: float = Column(Float)
    frete: float = Column(Float)
    id_produto: int = Column(Integer, ForeignKey('produtos.id'))
    id_loja: int = Column(Integer, ForeignKey('lojas.id'))

    produtos = relationship('ProdutoModel', back_populates='vendas', lazy='subquery')
    lojas = relationship('LojaModel', back_populates='vendas', lazy='subquery')



