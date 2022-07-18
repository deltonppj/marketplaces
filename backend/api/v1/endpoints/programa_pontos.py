from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.programa_pontos_repository import ProgramaPontosRepository
from schemas.programa_pontos_schema import ProgramaPontosSchema, ProgramaPontosSchemaRead

from core.deps import get_session, get_current_user

router = APIRouter()


# Criar programa de pontos
@router.post("/", response_model=ProgramaPontosSchema, status_code=status.HTTP_201_CREATED)
async def post_programa_pontos(programa_pontos: ProgramaPontosSchema,
                               is_logged=Depends(get_current_user),
                               db: AsyncSession = Depends(get_session)):
    """
    Este endpoint cria um novo programa de pontos no banco de dados.
    """
    return await ProgramaPontosRepository(db).create_programa_pontos(programa_pontos)


# Pegar todos os programas de pontos
@router.get("/", response_model=List[ProgramaPontosSchema])
async def get_programas_pontos(db: AsyncSession = Depends(get_session),
                               is_logged=Depends(get_current_user)):
    """
    Este endpoint retorna todos os programas de pontos do banco de dados.
    """
    return await ProgramaPontosRepository(db).list_programa_pontos()


# Pegar um programa de pontos pelo id
@router.get("/{programa_pontos_id}", response_model=ProgramaPontosSchema, status_code=status.HTTP_200_OK)
async def get_programa_pontos(programa_pontos_id: int,
                              is_logged=Depends(get_current_user),
                              db: AsyncSession = Depends(get_session)):
    """
    Este endpoint retorna um programa de pontos através do seu id.
    """
    programa_pontos = await ProgramaPontosRepository(db).get_programa_pontos_by_id(programa_pontos_id)

    if programa_pontos:
        return programa_pontos
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Programa de pontos não encontrado")


# Pegar um programa de pontos pelo nome
@router.get("/nome/{nome}", response_model=List[ProgramaPontosSchemaRead], status_code=status.HTTP_200_OK)
async def get_programa_pontos_nome(nome: str,
                                   is_logged=Depends(get_current_user),
                                   db: AsyncSession = Depends(get_session)):
    """
    Este endpoint retorna um programa de pontos através do seu nome.
    """
    return await ProgramaPontosRepository(db).get_programa_pontos_by_nome(nome)


# Update um programa de pontos
@router.put("/{programa_pontos_id}", response_model=ProgramaPontosSchema, status_code=status.HTTP_200_OK)
async def update_programa_pontos(programa_pontos_id: int,
                                 programa_pontos: ProgramaPontosSchema,
                                 is_logged=Depends(get_current_user),
                                 db: AsyncSession = Depends(get_session)):
    """
    Este endpoint atualiza um programa de pontos através do seu id.
    """
    programa_pontos = await ProgramaPontosRepository(db).update_programa_pontos(programa_pontos_id, programa_pontos)

    if programa_pontos:
        return programa_pontos
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Programa de pontos não encontrado")


# Delete um programa de pontos
@router.delete("/{programa_pontos_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_programa_pontos(programa_pontos_id: int,
                                 is_logged=Depends(get_current_user),
                                 db: AsyncSession = Depends(get_session)):
    """
    Este endpoint deleta um programa de pontos através do seu id.
    """
    programa_pontos_del = await ProgramaPontosRepository(db).delete_programa_pontos(programa_pontos_id)
    if programa_pontos_del:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Programa de pontos não encontrado")
