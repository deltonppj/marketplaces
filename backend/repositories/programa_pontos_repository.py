from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from sqlalchemy import and_
from sqlalchemy import inspect

from models.programa_pontos_model import ProgramaPontosModel, LojaProgramaPontos
from models.loja_model import LojaModel
from repositories.loja_repository import LojaRepository
from schemas.programa_pontos_schema import ProgramaPontosSchema, LojaProgramaPontosSchema, ProgramaPontosSchemaRead, \
    LojaProgramaPontosCreateSchema


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

    async def create_programa_pontos_by_loja(self, loja_programa_pontos: LojaProgramaPontosCreateSchema):

        async with self.db as session:
            try:
                # Atualiza
                loja = await LojaRepository(self.db).get_loja_by_nome(loja_programa_pontos.loja_nome)
                programa_pontos = await self.get_programa_pontos_by_nome(loja_programa_pontos.programa_pontos_nome)

                query = select(LojaProgramaPontos) \
                    .filter(LojaProgramaPontos.id_loja == loja.id) \
                    .filter(LojaProgramaPontos.id_programa_pontos == programa_pontos.id)
                result = await session.execute(query)
                loja_pp_atual: LojaProgramaPontos = result.scalars().unique().one_or_none()

                if loja_pp_atual:
                    loja_pp_atual.valor_bonus = loja_programa_pontos.valor_bonus
                    loja_pp_atual.valor_real = loja_programa_pontos.valor_real
                    await session.commit()
                    return loja_pp_atual
                else:
                    # Cria
                    lpp = LojaProgramaPontos(valor_bonus=loja_programa_pontos.valor_bonus,
                                             valor_real=loja_programa_pontos.valor_real)
                    lpp.ppm = programa_pontos
                    loja.ppms.append(lpp)
                    session.add(loja)
                    await session.commit()
                    await session.refresh(lpp)
                    return lpp  # LojaProgramaPontosSchema
            except Exception:
                return None

    async def list_programa_pontos_by_loja(self, loja_nome: str):
        loja = await LojaRepository(self.db).get_loja_by_nome(loja_nome)
        async with self.db as session:
            query = select(LojaProgramaPontos) \
                .join(ProgramaPontosModel, LojaProgramaPontos.id_loja == loja.id) \
                .order_by(LojaProgramaPontos.created_at.desc())
            result = await session.execute(query)
            loja_programa_pontos: List[LojaProgramaPontos] = result.scalars().unique().all()
            return loja_programa_pontos

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
            query = select(ProgramaPontosModel) \
                .filter(ProgramaPontosModel.nome.ilike(f'%{nome}%'))
            result = await session.execute(query)
            programa_pontos: ProgramaPontosModel = result.scalars().unique().one_or_none()
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
