from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from banco import Base


# Este modelo representa a tabela de pessoas que escolhem um perfil no sistema.
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    senha_hash = Column(String(255), nullable=True)

    # Esta relação permite acessar as coletas pertencentes ao morador pelo objeto.
    coletas = relationship("Coleta")
