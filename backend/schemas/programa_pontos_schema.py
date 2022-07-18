from typing import Optional

from pydantic import BaseModel as SCBaseModel


class ProgramaPontosSchema(SCBaseModel):
    id: Optional[int]
    nome: str

    class Config:
        orm_mode = True


class ProgramaPontosSchemaRead(SCBaseModel):
    id: Optional[int]
    nome: Optional[str]

    class Config:
        orm_mode = True


class LojaProgramaPontosSchema(SCBaseModel):
    id: Optional[int]
    id_loja: Optional[int]
    id_programa_pontos: Optional[int]
    valor_bonus: Optional[float]
    valor_real: Optional[float]

    class Config:
        orm_mode = True
