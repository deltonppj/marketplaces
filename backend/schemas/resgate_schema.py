from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel


class ResgateSchema(SCBaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    product_sku: str
    product_name: str
    product_reedem: float
    product_url: str

    class Config:
        orm_mode = True
