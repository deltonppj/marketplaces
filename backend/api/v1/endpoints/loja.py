from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from repositories.loja_repository import LojaRepository
from schemas.loja_schema import LojaSchema

from core.deps import get_session

router = APIRouter()


# Criar loja
@router.post("/", response_model=LojaSchema, status_code=status.HTTP_201_CREATED)
async def post_loja(loja: LojaSchema, db: AsyncSession = Depends(get_session)):
    return await LojaRepository(db).create_loja(loja)


# Pegar todas as lojas
@router.get("/", response_model=List[LojaSchema])
async def get_lojas(db: AsyncSession = Depends(get_session)):
    return await LojaRepository(db).list_lojas()


# Pegar uma loja
@router.get("/{loja_id}", response_model=LojaSchema, status_code=status.HTTP_200_OK)
async def get_loja(loja_id: int, db: AsyncSession = Depends(get_session)):
    loja = await LojaRepository(db).get_loja(loja_id)

    if loja:
        return loja
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")


# Atualizar loja
@router.put("/{loja_id}", response_model=LojaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_loja(loja_id: int, loja: LojaSchema, db: AsyncSession = Depends(get_session)):
    loja_atual = await LojaRepository(db).update_loja(loja_id, loja)
    if loja_atual:
        return loja_atual
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")


# Deletar loja
@router.delete("/{loja_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_loja(loja_id: int, db: AsyncSession = Depends(get_session)):
    loja_del = await LojaRepository(db).delete_loja(loja_id)
    if loja_del:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")
