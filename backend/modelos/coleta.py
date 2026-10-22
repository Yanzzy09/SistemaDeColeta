from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from banco import Base
from modelos.usuario import Usuario


# Este modelo representa uma coleta agendada por um morador.
class Coleta(Base):
    __tablename__ = "coletas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    morador_id = Column(
        Integer,
        ForeignKey("usuarios.id", name="fk_coletas_morador"),
        nullable=False,
    )
    endereco = Column(String(200), nullable=False)
    dia = Column(Date, nullable=False)
    materiais = Column(String(200), nullable=False)
    situacao = Column(String(20), nullable=False)
    pontos = Column(Integer, nullable=False, default=0)

    # Esta relação permite acessar o morador dono da coleta pelo objeto.
    morador = relationship("Usuario")

    # Esta relação permite acessar as pesagens ligadas à coleta.
    pesagens = relationship("Pesagem")
