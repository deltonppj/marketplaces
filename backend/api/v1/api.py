from fastapi import APIRouter

from api.v1.endpoints import loja
from api.v1.endpoints import produto

api_router = APIRouter()
api_router.include_router(loja.router, prefix="/lojas", tags=["lojas"])
api_router.include_router(produto.router, prefix="/produtos", tags=["produtos"])