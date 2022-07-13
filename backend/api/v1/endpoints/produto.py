from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.produto_model import ProdutoModel
from repositories.produto_repository import ProdutoRepository
from schemas.produto_schema import ProdutoSchema, CreateProdutoSchema, ReadProdutoSchema, UpdateProdutoSchema

from core.deps import get_session

router = APIRouter()


# Inserir um novo produto
@router.post('/', response_model=ProdutoSchema, status_code=status.HTTP_201_CREATED)
async def post_produto(produto: CreateProdutoSchema, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint cria um novo produto no banco de dados.
    """
    produto = await ProdutoRepository(db).create_produto(produto)
    if produto:
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")


# Listar todos os produtos
@router.get('/', response_model=List[ReadProdutoSchema])
async def get_produtos(db: AsyncSession = Depends(get_session), limit: int = 10, offset: int = 0):
    """
    Este endpoint retorna todos os produtos do banco de dados limitado por paginação.
    """
    return await ProdutoRepository(db).list_produtos(limit, offset)


# Listar um produto pelo id
@router.get('/{produto_id}', response_model=ReadProdutoSchema, status_code=status.HTTP_200_OK)
async def get_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint retorna um produto através do seu id.
    """
    produto = await ProdutoRepository(db).get_produto(produto_id)
    if produto:
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")


# Listar um produto pelo sku
@router.get('/sku/{sku}', response_model=List[ReadProdutoSchema], status_code=status.HTTP_200_OK)
async def get_produto_by_sku(sku: str, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint retorna um produto através do seu sku.
    """
    produto = await ProdutoRepository(db).get_produto_by_sku(sku)
    if produto:
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")


# Listar produto pelo nome
@router.get('/nome/{nome}', response_model=List[ReadProdutoSchema])
async def get_produto_by_nome(nome: str, db: AsyncSession = Depends(get_session), limit: int = 10, offset: int = 0):
    """
    Este endpoint retorna um produto através do seu nome.
    """
    return await ProdutoRepository(db).get_produto_by_nome(nome, limit, offset)


# Atualizar um produto
@router.put('/{produto_id}', response_model=ReadProdutoSchema, status_code=status.HTTP_200_OK)
async def put_produto(produto_id: int, produto: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint atualiza um produto através do seu id.
    """
    produto = await ProdutoRepository(db).update_produto(produto_id, produto)
    if produto:
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")


# Deletar um produto
@router.delete('/{produto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(produto_id: int, db: AsyncSession = Depends(get_session)):
    """
    Este endpoint deleta um produto através do seu id.
    """
    produto = await ProdutoRepository(db).delete_produto(produto_id)
    if produto:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
