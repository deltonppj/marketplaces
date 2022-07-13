from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from core.configs import settings


class ShopMilhasModel(settings.DBBaseModel):
    __tablename__: str = 'shopmilhas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    product_sku: str = Column(String(100), nullable=False)
    product_name: str = Column(String(250), nullable=False)
    product_price_sale: float = Column(Float, nullable=False)
    product_gain_miles: float = Column(Float, nullable=False)
    product_url: str = Column(String(250), nullable=False)