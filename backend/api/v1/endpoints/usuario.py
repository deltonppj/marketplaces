from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends, status, Response

from repositories.usuario_repository import UsuarioRepository
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate

from core.deps import get_session

router = APIRouter()


# Signup
@router.post("/signup", response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint cria um novo usuário no banco de dados.
    """
    usuario = await UsuarioRepository(db).create_usuario(usuario)
    if usuario:
        return usuario
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Já existe um usuário cadastrado com este email.')

