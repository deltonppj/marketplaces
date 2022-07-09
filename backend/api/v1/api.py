from fastapi import APIRouter

from api.v1.endpoints import loja

api_router = APIRouter()
api_router.include_router(loja.router, prefix="/lojas", tags=["lojas"])