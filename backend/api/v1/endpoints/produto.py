from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.loja_model import LojaModel
from schemas.loja_schema import LojaSchema
from models.produto_model import ProdutoModel
from schemas.produto_schema import ProdutoSchema

from core.deps import get_session

router = APIRouter()


@router.post('/', response_model=ProdutoSchema, status_code=status.HTTP_201_CREATED)
async def post_produto(produto: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        loja = await session.query(LojaModel).filter(LojaModel.nome == produto.id_loja).first()

        if loja:
            novo_produto = ProdutoModel(id_loja=loja.id, sku=produto.sku, name=produto.name, price=produto.price, url=produto.url)
            session.add(novo_produto)
            await session.commit()

            return novo_produto
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")
