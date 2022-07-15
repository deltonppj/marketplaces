from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from repositories.usuario_repository import UsuarioRepository
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate

from core.deps import get_session
from providers.hash_provider import check_hash

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


# Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    """
    Este endpoint retorna um usuário através do seu email.
    """
    usuario = await UsuarioRepository(db).get_usuario_by_email(form_data.username)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if not check_hash(form_data.password, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")

    return JSONResponse(content={"token": "implementar", "token_type": "bearer"}, status_code=status.HTTP_200_OK)