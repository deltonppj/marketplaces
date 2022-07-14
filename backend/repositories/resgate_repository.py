from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from models.resgate_model import ResgateModel
from schemas.resgate_schema import ResgateSchema


class ResgateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_produto(self, produto: ResgateSchema):
        async with self.db as session:
            novo_produto = ResgateModel(
                product_sku=produto.product_sku,
                product_name=produto.product_name,
                product_reedem=produto.product_reedem,
                product_url=produto.product_url
            )
            session.add(novo_produto)
            await session.commit()
            session.refresh(novo_produto)
            return novo_produto

    async def list_produtos(self, limit: int = 10, offset: int = 0):
        async with self.db as session:
            query = select(ResgateModel) \
                .order_by(ResgateModel.created_at.desc()) \
                .order_by(ResgateModel.product_reedem.asc())
            result = await session.execute(query)
            produtos: List[ResgateModel] = result.scalars().unique().all()
            return produtos[offset:offset + limit]

    async def get_produto_by_nome(self, name: str, limit: int = 10, offset: int = 0):
        async with self.db as session:
            name = name.split(' ')
            query = select(ResgateModel)\
                .filter(and_(*[ResgateModel.product_name.ilike('%' + nome + ' %') for nome in name])) \
                .order_by(ResgateModel.created_at.desc()) \
                .order_by(ResgateModel.product_reedem.asc())
            result = await session.execute(query)
            produto: ResgateModel = result.scalars().unique().all()
            return produto[offset:offset + limit]

    async def update_produto(self, produto_id: int, produto: ResgateSchema):
        async with self.db as session:
            query = select(ResgateModel).filter(ResgateModel.id == produto_id)
            result = await session.execute(query)
            produto_atual: ResgateModel = result.scalars().unique().one_or_none()
            if produto_atual:
                produto_atual.product_sku = produto.product_sku
                produto_atual.product_name = produto.product_name
                produto_atual.product_reedem = produto.product_reedem
                produto_atual.product_url = produto.product_url
                await session.commit()

    async def delete_produto(self, produto_id: int):
        async with self.db as session:
            query = select(ResgateModel).filter(ResgateModel.id == produto_id)
            result = await session.execute(query)
            produto: ResgateModel = result.scalars().unique().one_or_none()
            if produto:
                await session.delete(produto)
                await session.commit()
                return True
