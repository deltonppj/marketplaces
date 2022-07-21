from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel

from schemas.produto_schema import ProdutoVendaSchema
from schemas.loja_schema import LojaVendaSchema


class VendaSchema(SCBaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    loja_id: int
    produto_id: int
    programa_pontos_id: int
    preco_venda: Optional[float] = 0.0
    frete: Optional[float] = 0.0

    class Config:
        orm_mode = True


class VendaSchemaRead(SCBaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    preco_venda: Optional[float] = 0.0
    frete: Optional[float] = 0.0
    produtos: ProdutoVendaSchema
    lojas: LojaVendaSchema

    class Config:
        orm_mode = True
