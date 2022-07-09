from datetime import datetime

from core.settings import settings

from sqlalchemy import Column, Integer, String, Float, DateTime


class ProdutoModel(settings.DBBaseModel):
    __tablename__: str = 'produtos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    sku: str = Column(String(100), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    name: str = Column(String(100), nullable=False, uniuque=True)
    price: float = Column(Float, nullable=False)
    url: str = Column(String(100), nullable=False)