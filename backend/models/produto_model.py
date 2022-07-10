from datetime import datetime

from core.configs import settings
from models.loja_model import LojaModel

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class ProdutoModel(settings.DBBaseModel):
    __tablename__: str = 'produtos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    sku: str = Column(String(100), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    name: str = Column(String(100), nullable=False, unique=True)
    price: float = Column(Float, nullable=False)
    url: str = Column(String(100), nullable=False)
    id_loja: int = Column(Integer, ForeignKey('lojas.id'))
    loja_model: LojaModel = relationship(LojaModel, back_populates='produtos', lazy='joined')
