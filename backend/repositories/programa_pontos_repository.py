from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from models.programa_pontos_model import ProgramaPontosModel
from schemas.programa_pontos_schema import ProgramaPontosSchema, LojaProgramaPontosSchema, ProgramaPontosSchemaRead


class ProgramaPontosRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_programa_pontos(self, programa_pontos: ProgramaPontosSchema):
        async with self.db as session:
            novo_programa_pontos = ProgramaPontosModel(nome=programa_pontos.nome)
            session.add(novo_programa_pontos)
            await session.commit()
            session.refresh(novo_programa_pontos)
            return novo_programa_pontos

    async def list_programa_pontos(self):
        async with self.db as session:
            query = select(ProgramaPontosModel)
            result = await session.execute(query)
            programa_pontos: List[ProgramaPontosModel] = result.scalars().unique().all()
            return programa_pontos

    async def get_programa_pontos_by_id(self, programa_pontos_id: int):
        async with self.db as session:
            query = select(ProgramaPontosModel).filter(ProgramaPontosModel.id == programa_pontos_id)
            result = await session.execute(query)
            programa_pontos: ProgramaPontosModel = result.scalars().unique().one_or_none()
            return programa_pontos

    async def get_programa_pontos_by_nome(self, nome: str):
        async with self.db as session:
            name = nome.split(' ')

            query = select(ProgramaPontosModel).\
                filter(and_(*[ProgramaPontosModel.nome.ilike('%' + nome + ' %') for nome in name]))
            result = await session.execute(query)
            programa_pontos: ProgramaPontosModel = result.scalars().unique().all()
            return programa_pontos

    async def update_programa_pontos(self, programa_pontos_id: int, programa_pontos: ProgramaPontosSchema):
        async with self.db as session:
            query = select(ProgramaPontosModel).filter(ProgramaPontosModel.id == programa_pontos_id)
            result = await session.execute(query)
            programa_pontos_atual: ProgramaPontosModel = result.scalars().unique().one_or_none()
            if programa_pontos_atual:
                programa_pontos_atual.nome = programa_pontos.nome
                await session.commit()

            return programa_pontos_atual

    async def delete_programa_pontos(self, programa_pontos_id: int):
        async with self.db as session:
            query = select(ProgramaPontosModel).filter(ProgramaPontosModel.id == programa_pontos_id)
            result = await session.execute(query)
            programa_pontos_del: ProgramaPontosModel = result.scalars().unique().one_or_none()
            if programa_pontos_del:
                await session.delete(programa_pontos_del)
                await session.commit()
                return True