from datetime import datetime
from typing import List

from core.configs import settings

from models.loja_model import LojaModel

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy import Table
from sqlalchemy.orm import relationship

# Uma loja tem vários programas de pontos
loja_programa_pontos = Table(
    'loja_programa_pontos',
    settings.DBBaseModel.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('CreatedAt', DateTime, default=datetime.now, index=True),
    Column('id_loja', Integer, ForeignKey('lojas.id')),
    Column('id_programas_pontos', Integer, ForeignKey('programas_pontos.id')),
    Column('valor_bonus', Float, nullable=False),
    Column('valor_real', Float, nullable=False),
)


class ProgramaPontosModel(settings.DBBaseModel):
    __tablename__: str = 'programas_pontos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False, unique=True)

    lojas: List[LojaModel] = relationship('LojaModel',
                                          secondary=loja_programa_pontos,
                                          backref='loja_model',
                                          lazy='dynamic')
