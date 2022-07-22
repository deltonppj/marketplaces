from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.venda_repository import VendaRepository
from schemas.venda_schema import VendaSchemaRead

from core.deps import get_session, get_current_user

router = APIRouter()


@router.get("/criar-lista-de-hoje", response_model=List[VendaSchemaRead])
async def criar_today_list(db: AsyncSession = Depends(get_session)):
    """
    Cria uma lista com os produtos de hoje
    """
    result = await VendaRepository(db).criar_today_list()
    if result:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar lista de hoje")


@router.get("/", response_model=List[VendaSchemaRead])
async def list_vendas(db: AsyncSession = Depends(get_session)):
    """
    Este endpoint retorna todas as vendas do dia atual.
    """
    return await VendaRepository(db).list_vendas()