from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel


class ProdutoSchema(SCBaseModel):
    id: Optional[int]
    id_loja: Optional[int]
    product_sku: str
    created_at: Optional[datetime]
    product_name: str
    product_price_sale: float
    product_url: str

    class Config:
        orm_mode = True


class ProdutoSchemaLoja(ProdutoSchema):
    id_loja: str


class ProdutoSchemaUrl(SCBaseModel):
    product_url: str

    class Config:
        orm_mode = True
