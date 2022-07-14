from fastapi import APIRouter

from api.v1.endpoints import loja
from api.v1.endpoints import produto
from api.v1.endpoints import shopmilhas
from api.v1.endpoints import resgate

api_router = APIRouter()
api_router.include_router(loja.router, prefix="/lojas", tags=["lojas"])
api_router.include_router(produto.router, prefix="/produtos", tags=["produtos"])
api_router.include_router(shopmilhas.router, prefix="/shopmilhas", tags=["shopmilhas"])
api_router.include_router(resgate.router, prefix="/resgates", tags=["resgates"])