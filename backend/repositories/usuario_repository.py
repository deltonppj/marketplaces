from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaCreate, UsuarioSchemaUpdate
from providers.hash_provider import hash_generator


class UsuarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_usuario(self, usuario: UsuarioSchemaCreate):
        novo_usuario = UsuarioModel(
            nome=usuario.nome,
            email=usuario.email,
            is_admin=usuario.is_admin,
            senha=hash_generator(usuario.senha))

        async with self.db as session:
            try:
                session.add(novo_usuario)
                await session.commit()
                session.refresh(novo_usuario)
                return novo_usuario
            except IntegrityError:
                return None

    async def list_usuarios(self):
        async with self.db as session:
            query = select(UsuarioModel)
            result = await session.execute(query)
            usuarios: List[UsuarioModel] = result.scalars().unique().all()
            return usuarios

    async def get_usuario(self, usuario_id: int):
        async with self.db as session:
            query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
            result = await session.execute(query)
            usuario: UsuarioModel = result.scalars().unique().one_or_none()
            return usuario

    async def update_usuario(self, usuario_id: int, usuario: UsuarioSchemaUpdate):
        async with self.db as session:
            query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
            result = await session.execute(query)
            usuario_atual: UsuarioModel = result.scalars().unique().one_or_none()
            if usuario_atual:
                if usuario.nome:
                    usuario_atual.nome = usuario.nome
                if usuario.email:
                    usuario_atual.email = usuario.email
                if usuario.senha:
                    usuario_atual.senha = hash_generator(usuario.senha)
                if usuario.is_admin:
                    usuario_atual.is_admin = usuario.is_admin

                await session.commit()
                return usuario_atual
            return None

    async def delete_usuario(self, usuario_id: int):
        async with self.db as session:
            query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
            result = await session.execute(query)
            usuario_del: UsuarioModel = result.scalars().unique().one_or_none()
            if usuario_del:
                await session.delete(usuario_del)
                await session.commit()
                return True
            return False
