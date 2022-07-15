from typing import Generator

from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,  HTTPException, status

from core.database import Session
from core.configs import settings
from models.usuario_model import UsuarioModel
from repositories.usuario_repository import UsuarioRepository
from schemas.usuario_schema import TokenData

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login/access-token"
)


async def get_session() -> Generator:
    """
    Get a new session from the database.
    """
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(reusable_oauth2)) -> UsuarioModel:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível autenticar o usuário',
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             settings.JWT_SECRET_KEY,
                             algorithms=[settings.ALGORITHM],
                             options={'verify_aud': False})
        usuario_id: int = payload.get('sub')

        if not usuario_id:
            raise credential_exception

        token_data: TokenData = TokenData(usuario_id=usuario_id)

    except JWTError:
        raise credential_exception

    usuario: UsuarioModel = await UsuarioRepository(db).get_usuario_by_id(int(token_data.usuario_id))

    if usuario is None:
        raise credential_exception

    return usuario
