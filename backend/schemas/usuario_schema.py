from typing import List
from typing import Optional

from pydantic import BaseModel as SCBaseModel, EmailStr


class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int]
    nome: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaUpdate(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    is_admin: Optional[bool]
