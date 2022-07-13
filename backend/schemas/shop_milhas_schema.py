from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel


class ShopMilhasSchema(SCBaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    product_sku: str
    product_name: str
    product_price_sale: float
    product_gain_miles: float
    product_url: str

    class Config:
        orm_mode = True
