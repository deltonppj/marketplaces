from core.settings import settings

from sqlalchemy import Column, Integer, String, Float

from models.loja_model import LojaModel


class ProgramaPontosModels(settings.DBBaseModel):
    __tablename__: str = 'programas_pontos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_loja: int = Column(Integer, ForeignKey('lojas.id'))
    loja_model: LojaModel = relationship('LojaModel', lazy='joined')

    nome: str = Column(String(100), nullable=False, uniuque=True)
    pontos_por_real: float = Column(Float, nullable=False)