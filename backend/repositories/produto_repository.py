from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy import func

from datetime import timedelta, datetime, date

from models.produto_model import ProdutoModel
from schemas.produto_schema import ProdutoSchema, CreateProdutoSchema
from repositories.loja_repository import LojaRepository


class ProdutoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_produto(self, produto: CreateProdutoSchema):
        loja = await LojaRepository(self.db).get_loja_by_nome(produto.loja_nome)
        if loja:
            async with self.db as session:
                novo_produto = ProdutoModel(
                    id_loja=loja.id,
                    product_sku=produto.product_sku,
                    product_name=produto.product_name,
                    product_price_sale=produto.product_price_sale,
                    product_url=produto.product_url)

                session.add(novo_produto)
                await session.commit()
                session.refresh(novo_produto)
                return novo_produto
        else:
            return None

    async def list_produtos_today(self):
        async with self.db as session:
            query = select(ProdutoModel).filter(func.date(ProdutoModel.created_at) == date.today())
            result = await session.execute(query)
            produtos: List[ProdutoModel] = result.scalars().unique().all()
            return produtos

    async def list_produtos(self, limit: int = 10, offset: int = 0):
        async with self.db as session:
            query = select(ProdutoModel) \
                .order_by(ProdutoModel.created_at.desc()) \
                .order_by(ProdutoModel.product_price_sale.asc())

            result = await session.execute(query)
            produtos: List[ProdutoModel] = result.scalars().unique().all()
            return produtos[offset:offset + limit]

    async def get_produto(self, produto_id: int):
        async with self.db as session:
            query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
            result = await session.execute(query)
            produto: ProdutoModel = result.scalars().unique().one_or_none()
            return produto

    async def get_produto_by_sku(self, sku: str):
        async with self.db as session:
            query = select(ProdutoModel).filter(ProdutoModel.product_sku == sku)
            result = await session.execute(query)
            produto: ProdutoModel = result.scalars().unique().all()
            return produto

    async def get_produto_by_nome(self, name: str, limit: int = 10, offset: int = 0):
        async with self.db as session:
            name = name.split(' ')

            query = select(ProdutoModel)\
                .filter(and_(*[ProdutoModel.product_name.ilike('%' + nome + ' %') for nome in name])) \
                .order_by(ProdutoModel.created_at.desc()) \
                .order_by(ProdutoModel.product_price_sale.asc())

            result = await session.execute(query)
            produto: ProdutoModel = result.scalars().unique().all()
            return produto[offset:offset + limit]

    async def update_produto(self, produto_id: int, produto: ProdutoSchema):
        async with self.db as session:
            query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
            result = await session.execute(query)
            produto_atual: ProdutoModel = result.scalars().unique().one_or_none()
            if produto_atual:
                produto_atual.product_sku = produto.product_sku
                produto_atual.product_name = produto.product_name
                produto_atual.product_price_sale = produto.product_price_sale
                produto_atual.product_url = produto.product_url
                await session.commit()

            return produto_atual

    async def delete_produto(self, produto_id: int):
        async with self.db as session:
            query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
            result = await session.execute(query)
            produto: ProdutoModel = result.scalars().unique().one_or_none()
            if produto:
                await session.delete(produto)
                await session.commit()
                return True
