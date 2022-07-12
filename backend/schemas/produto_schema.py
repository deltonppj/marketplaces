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


class CreateProdutoSchema(SCBaseModel):
    id: Optional[int]
    loja_nome: str
    product_sku: str
    created_at: Optional[datetime]
    product_name: str
    product_price_sale: float
    product_url: str

    class Config:
        orm_mode = True


class ReadProdutoSchema(SCBaseModel):
    id: Optional[int]
    product_sku: str
    created_at: Optional[datetime]
    product_name: str
    product_price_sale: float
    product_url: str

    class Config:
        orm_mode = True


class UpdateProdutoSchema(SCBaseModel):
    product_sku: Optional[str]
    created_at: Optional[datetime]
    product_name: Optional[str]
    product_price_sale: Optional[float]
    product_url: Optional[str]

    class Config:
        orm_mode = True


class ProdutoSchemaLoja(ProdutoSchema):
    id_loja: str


class ProdutoSchemaUrl(SCBaseModel):
    product_url: str

    class Config:
        orm_mode = True
