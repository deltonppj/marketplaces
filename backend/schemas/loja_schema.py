from typing import Optional
from typing import List

from pydantic import BaseModel as SCBaseModel
from schemas.produto_schema import ProdutoSchema


class LojaSchema(SCBaseModel):
    id: Optional[int]
    nome: str

    class Config:
        orm_mode = True


class LojaSchemaProduto(LojaSchema):
    produtos: Optional[List[ProdutoSchema]]
