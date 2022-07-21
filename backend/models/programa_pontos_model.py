from datetime import datetime
from typing import List

from core.configs import settings

from models.loja_model import LojaModel

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy import Table
from sqlalchemy.orm import relationship


# # Uma loja tem vários programas de pontos
# loja_programa_pontos = Table(
#     'loja_programa_pontos',
#     settings.DBBaseModel.metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('CreatedAt', DateTime, default=datetime.now, index=True),
#     Column('id_loja', Integer, ForeignKey('lojas.id')),
#     Column('id_programas_pontos', Integer, ForeignKey('programas_pontos.id')),
#     Column('valor_bonus', Float, nullable=False),
#     Column('valor_real', Float, nullable=False),
# )


class LojaProgramaPontos(settings.DBBaseModel):
    __tablename__ = 'loja_programa_pontos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    valor_bonus: float = Column(Float, nullable=False)
    valor_real: float = Column(Float, nullable=False)

    id_loja: int = Column(Integer, ForeignKey('lojas.id'))
    id_programa_pontos: int = Column(Integer, ForeignKey('programas_pontos.id'))

    loja = relationship('LojaModel', back_populates='ppms', lazy='joined')
    ppm = relationship('ProgramaPontosModel', back_populates='ljs', lazy='joined')


class ProgramaPontosModel(settings.DBBaseModel):
    __tablename__: str = 'programas_pontos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)

    ljs = relationship('LojaProgramaPontos', back_populates='ppm')
