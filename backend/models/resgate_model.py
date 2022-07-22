from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from core.configs import settings


class ResgateModel(settings.DBBaseModel):
    __tablename__: str = 'resgates'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    product_sku: str = Column(String(100), nullable=False)
    product_name: str = Column(String(500), nullable=False)
    product_reedem: float = Column(Float, nullable=False)
    product_url: str = Column(String(500), nullable=False)
