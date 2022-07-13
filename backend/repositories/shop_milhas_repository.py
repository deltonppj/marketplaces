from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from models.shop_milhas_model import ShopMilhasModel
from schemas.shop_milhas_schema import ShopMilhasSchema


class ShopMilhasRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


async def create_produto(self, produto: ShopMilhasSchema):
    async with self.db as session:
        novo_produto = ShopMilhasModel(
            product_sku=produto.product_sku,
            product_name=produto.product_name,
            product_price_sale=produto.product_price_sale,
            product_gain_miles=produto.product_gain_miles,
            product_url=produto.product_url
        )
        await session.add(novo_produto)
        await ssession.commit()
        session.refresh(novo_produto)
        return novo_produto


async def list_produtos(self, limit: int = 10, offset: int = 0):
    async with self.db as session:
        query = select(ShopMilhasModel)
        result = await session.execute(query)
        produtos: List[ShopMilhasModel] = result.scalars().unique().all()
        return produtos[offset:offset + limit]


async def update_produto(self, produto_id: int, produto: ShopMilhasSchema):
    async with self.db as session:
        query = select(ShopMilhasModel).filter(ShopMilhasModel.id == produto_id)
        result = await session.execute(query)
        produto_atual: ShopMilhasModel = result.scalars().unique().one_or_none()
        if produto_atual:
            produto_atual.product_sku = produto.product_sku
            produto_atual.product_name = produto.product_name
            produto_atual.product_price_sale = produto.product_price_sale
            produto_atual.product_gain_miles = produto.product_gain_miles
            produto_atual.product_url = produto.product_url
            await session.commit()

        return produto_atual


async def delete_produto(self, produto_id: int):
    async with self.db as session:
        query = select(ShopMilhasModel).filter(ShopMilhasModel.id == produto_id)
        result = await session.execute(query)
        produto: ShopMilhasModel = result.scalars().unique().one_or_none()
        if produto:
            await session.delete(produto)
            await session.commit()
            return True
