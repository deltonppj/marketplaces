from sqlalchemy import Column, Integer, String, Boolean

from core.configs import settings


class UsuarioModel(settings.DBBaseModel):
    __tablename__: str = 'usuarios'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False, index=True, unique=True)
    senha: str = Column(String(100), nullable=False)
    is_admin: bool = Column(Boolean, nullable=False, default=False)
