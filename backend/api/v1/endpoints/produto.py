from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.loja_model import LojaModel
from models.produto_model import ProdutoModel
from schemas.produto_schema import ProdutoSchemaLoja

from core.deps import get_session

router = APIRouter()


# Inserir um novo produto
@router.post('/', response_model=ProdutoSchemaLoja, status_code=status.HTTP_201_CREATED)
async def post_produto(produto: ProdutoSchemaLoja, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LojaModel).filter(LojaModel.nome == produto.id_loja)
        result = await session.execute(query)
        loja: LojaModel = result.scalars().unique().one_or_none()

        if loja:
            novo_produto = ProdutoModel(id_loja=loja.id,
                                        product_sku=produto.product_sku,
                                        product_name=produto.product_name,
                                        product_price_sale=produto.product_price_sale,
                                        product_url=produto.product_url)
            session.add(novo_produto)
            await session.commit()

            return novo_produto
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")


# Listar todos os produtos
@router.get('/', response_model=List[ProdutoSchemaLoja])
async def get_produtos(db: AsyncSession = Depends(get_session), limit: int = 5, offset: int = 0):
    async with db as session:
        query = select(ProdutoModel)
        result = await session.execute(query)
        produtos: List[ProdutoModel] = result.scalars().unique().all()

        return produtos[offset: offset + limit]


# Listar um produto pelo nome
@router.get('/{name}', response_model=ProdutoSchemaLoja)
async def get_produto_by_name(name: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.product_name.ilike(f'%{name}%'))
        result = await session.execute(query)
        produto: ProdutoModel = result.scalars().unique().all()
        if produto:
            return produto
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
