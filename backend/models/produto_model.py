from datetime import datetime

from core.configs import settings
from models.loja_model import LojaModel
from models.venda_model import VendaModel

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class ProdutoModel(settings.DBBaseModel):
    __tablename__: str = 'produtos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_sku: str = Column(String(100), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    product_name: str = Column(String(250), nullable=False)
    product_price_sale: float = Column(Float, nullable=False)
    product_url: str = Column(String(350), nullable=False)

    id_loja: int = Column(Integer, ForeignKey('lojas.id'))

    loja_model: LojaModel = relationship(
        'LojaModel',
        back_populates='produtos',
        lazy='joined')

    vendas = relationship('VendaModel',
                         back_populates='produtos',
                         uselist=False)
