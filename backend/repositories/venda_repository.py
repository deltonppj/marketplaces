from datetime import datetime, date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy import func

from models.venda_model import VendaModel
from models.loja_model import LojaModel
from models.produto_model import ProdutoModel
from models.programa_pontos_model import LojaProgramaPontos

from schemas.venda_schema import VendaSchema

from repositories.produto_repository import ProdutoRepository
from repositories.loja_repository import LojaRepository
from repositories.programa_pontos_repository import ProgramaPontosRepository


class VendaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def criar_today_list(self):
        preco_venda = 0
        frete = 0

        try:
            list_produtos = await ProdutoRepository(self.db).list_produtos_today()

            for produto in list_produtos:
                async with self.db as session:
                    venda = VendaModel(
                        id_loja=produto.id_loja,
                        id_produto=produto.id,
                        preco_venda=preco_venda,
                        frete=frete)
                    session.add(venda)
                    await session.commit()
            return True
        except:
            return False

    async def list_vendas(self):
        async with self.db as session:
            query = select(VendaModel, ProdutoModel) \
                .filter(func.date(VendaModel.created_at) == date.today()) \
                .join(ProdutoModel, VendaModel.id_produto == ProdutoModel.id) \
                .join(LojaModel, VendaModel.id_loja == LojaModel.id) \
                .order_by(VendaModel.created_at.desc())
            result = await session.execute(query)
            vendas: List[VendaModel] = result.scalars().unique().all()
            return vendas
