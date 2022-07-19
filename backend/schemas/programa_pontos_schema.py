from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel
from schemas.loja_schema import LojaSchema


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
    valor_bonus: float
    valor_real: float

    class Config:
        orm_mode = True


class LojaProgramaPontosSchemaRead(SCBaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    valor_bonus: float
    valor_real: float
    loja: Optional[LojaSchema]
    ppm: Optional[ProgramaPontosSchemaRead]

    class Config:
        orm_mode = True


class LojaProgramaPontosCreateSchema(SCBaseModel):
    id: Optional[int]
    loja_nome: str
    programa_pontos_nome: str
    valor_bonus: float
    valor_real: float

    class Config:
        orm_mode = True
