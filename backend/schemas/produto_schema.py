from typing import Optional

from pydantic import BaseModel as SCBaseModel


class ProdutoSchema(SCBaseModel):
    id: Optional[int]
    id_loja: Optional[int]
    sku: str
    created_at: Optional[str]
    name: str
    price: float
    url: str

    class Config:
        orm_mode = True

