from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from models.shop_milhas_model import ShopMilhasModel
from repositories.shop_milhas_repository import ShopMilhasRepository
from schemas.shop_milhas_schema import ShopMilhasSchema

from core.deps import get_session

router = APIRouter()


# Inserir um novo produto
@router.post('/', response_model=ShopMilhasSchema, status_code=status.HTTP_201_CREATED)
async def post_produto(produto: ShopMilhasSchema, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint cria um novo produto na tabela shopmilhas.
    """
    return await ShopMilhasRepository(db).create_produto(produto)


# Listar todos os produtos
@router.get('/', response_model=List[ShopMilhasSchema])
async def get_produtos(db: AsyncSession = Depends(get_session), limit: int = 10, offset: int = 0):
    """
    Este endpoint retorna todos os produtos da tabela shopmilhas limitado por paginação.
    """
    return await ShopMilhasRepository(db).list_produtos(limit, offset)


# Listar produto pelo nome
@router.get('/nome/{nome}', response_model=List[ShopMilhasSchema])
async def get_produto_by_nome(nome: str, db: AsyncSession = Depends(get_session), limit: int = 10, offset: int = 0):
    """
    Este endpoint retorna um produto através do seu nome.
    """
    return await ShopMilhasRepository(db).get_produto_by_nome(nome, limit, offset)


# Update um produto
@router.put('/{produto_id}', response_model=ShopMilhasSchema, status_code=status.HTTP_200_OK)
async def update_produto(produto_id: int, produto: ShopMilhasSchema, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint atualiza um produto na tabela shopmilhas.
    """
    produto = ShopMilhasRepository(db).update_produto(produto_id, produto)
    if produto:
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")


# Delete um produto
@router.delete('/{produto_id}', status_code=status.HTTP_200_OK)
async def delete_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint deleta um produto na tabela shopmilhas.
    """
    result = await ShopMilhasRepository(db).delete_produto(produto_id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
