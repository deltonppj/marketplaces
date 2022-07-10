from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.loja_model import LojaModel
from schemas.loja_schema import LojaSchema
from core.deps import get_session

router = APIRouter()


# Criar loja
@router.post("/", response_model=LojaSchema, status_code=status.HTTP_201_CREATED)
async def post_loja(loja: LojaSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        nova_loja = LojaModel(nome=loja.nome)
        session.add(nova_loja)
        await session.commit()

        return nova_loja


# Pegar todas as lojas
@router.get("/", response_model=List[LojaSchema])
async def get_lojas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LojaModel)
        result = await session.execute(query)
        lojas: List[LojaModel] = result.scalars().all()
        return lojas


# Pegar uma loja
@router.get("/{loja_id}", response_model=LojaSchema, status_code=status.HTTP_200_OK)
async def get_loja(loja_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LojaModel).filter(LojaModel.id == loja_id)
        result = await session.execute(query)
        loja: LojaModel = result.scalar_one_or_none()

        if loja:
            return loja
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")


# Atualizar loja
@router.put("/{loja_id}", response_model=LojaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_loja(loja_id: int, loja: LojaSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LojaModel).filter(LojaModel.id == loja_id)
        result = await session.execute(query)
        loja_atual: LojaModel = result.scalar_one_or_none()

        if loja_atual:
            loja_atual.nome = loja.nome
            await session.commit()
            return loja_atual
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")


# Deletar loja
@router.delete("/{loja_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_loja(loja_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LojaModel).filter(LojaModel.id == loja_id)
        result = await session.execute(query)
        loja_del: LojaModel = result.scalar_one_or_none()

        if loja_del:
            await session.delete(loja_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loja não encontrada")
