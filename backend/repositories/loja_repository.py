from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.loja_model import LojaModel
from schemas.loja_schema import LojaSchema


class LojaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_loja(self, loja: LojaSchema):
        async with self.db as session:
            nova_loja = LojaModel(nome=loja.nome)
            session.add(nova_loja)
            await session.commit()
            session.refresh(nova_loja)
            return nova_loja

    async def list_lojas(self):
        async with self.db as session:
            query = select(LojaModel)
            result = await session.execute(query)
            lojas: List[LojaModel] = result.scalars().unique().all()
            return lojas

    async def get_loja(self, loja_id: int):
        async with self.db as session:
            query = select(LojaModel).filter(LojaModel.id == loja_id)
            result = await session.execute(query)
            loja: LojaModel = result.scalars().unique().one_or_none()
            return loja

    async def update_loja(self, loja_id: int, loja: LojaSchema):
        async with self.db as session:
            query = select(LojaModel).filter(LojaModel.id == loja_id)
            result = await session.execute(query)
            loja_atual: LojaModel = result.scalars().unique().one_or_none()
            if loja_atual:
                loja_atual.nome = loja.nome
                await session.commit()

            return loja_atual

    async def delete_loja(self, loja_id: int):
        async with self.db as session:
            query = select(LojaModel).filter(LojaModel.id == loja_id)
            result = await session.execute(query)
            loja_del: LojaModel = result.scalars().unique().one_or_none()
            if loja_del:
                await session.delete(loja_del)
                await session.commit()
                return True

