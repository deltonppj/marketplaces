from typing import Optional

from pydantic import BaseModel as SCBaseModel


class ProgramaPontosSchema(SCBaseModel):
    id: Optional[int]
    id_loja: Optional[int]
    nome: str
    pontos_por_real: float

    class Config:
        orm_mode = True
