from typing import Optional
from typing import List

from pydantic import BaseModel as SCBaseModel
from schemas.produto_schema import ProdutoSchemaUrl
from schemas.programa_pontos_schema import LojaProgramaPontosSchemaRead


class LojaSchema(SCBaseModel):
    id: Optional[int]
    nome: str

    class Config:
        orm_mode = True


class LojaSchemaProduto(LojaSchema):
    produtos: Optional[List[ProdutoSchemaUrl]]


class LojaNomeSchema(SCBaseModel):
    nome: str

    class Config:
        orm_mode = True


class LojaVendaSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    ppms: Optional[List[LojaProgramaPontosSchemaRead]]

    class Config:
        orm_mode = True
