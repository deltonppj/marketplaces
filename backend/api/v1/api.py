from fastapi import APIRouter

from api.v1.endpoints import loja
from api.v1.endpoints import produto
from api.v1.endpoints import shopmilhas
from api.v1.endpoints import resgate
from api.v1.endpoints import usuario
from api.v1.endpoints import programa_pontos
from api.v1.endpoints import venda

api_router = APIRouter()
api_router.include_router(loja.router, prefix="/lojas", tags=["lojas"])
api_router.include_router(produto.router, prefix="/produtos", tags=["produtos"])
api_router.include_router(shopmilhas.router, prefix="/shopmilhas", tags=["shopmilhas"])
api_router.include_router(resgate.router, prefix="/resgates", tags=["resgates"])
api_router.include_router(usuario.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(programa_pontos.router, prefix="/programaspontos", tags=["programas_pontos"])
api_router.include_router(venda.router, prefix="/vendas", tags=["vendas"])