from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from models.resgate_model import ResgateModel
from repositories.resgate_repository import ResgateRepository
from schemas.resgate_schema import ResgateSchema

from core.deps import get_session

router = APIRouter()


# Insirir um novo produto
@router.post('/', response_model=ResgateSchema, status_code=status.HTTP_201_CREATED)
async def post_produto(produto: ResgateSchema, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint cria um novo produto na tabela resgates.
    """
    return await ResgateRepository(db).create_produto(produto)


# Listar todos os produtos
@router.get('/', response_model=List[ResgateSchema])
async def get_produtos(db: AsyncSession = Depends(get_session), limit: int = 10, offset: int = 0):
    """
    Este endpoint retorna todos os produtos da tabela resgates limitado por paginação.
    """
    return await ResgateRepository(db).list_produtos(limit, offset)


# Listar produto pelo nome
@router.get('/nome/{nome}', response_model=List[ResgateSchema])
async def get_produto_by_nome(nome: str, db: AsyncSession = Depends(get_session), limit: int = 10, offset: int = 0):
    """
    Este endpoint retorna um produto através do seu nome.
    """
    return await ResgateRepository(db).get_produto_by_nome(nome, limit, offset)


# Update um produto
@router.put('/{produto_id}', response_model=ResgateSchema, status_code=status.HTTP_200_OK)
async def update_produto(produto_id: int, produto: ResgateSchema, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint atualiza um produto na tabela resgates.
    """
    produto = ResgateRepository(db).update_produto(produto_id, produto)
    if produto:
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")


# Delete um produto
@router.delete('/{produto_id}', status_code=status.HTTP_200_OK)
async def delete_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint deleta um produto na tabela resgates.
    """
    result = await ResgateRepository(db).delete_produto(produto_id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
