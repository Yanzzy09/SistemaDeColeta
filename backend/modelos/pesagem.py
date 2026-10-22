from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from banco import Base
from modelos.coleta import Coleta


# Este modelo representa um material pesado dentro de uma coleta.
class Pesagem(Base):
    __tablename__ = "pesagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coleta_id = Column(
        Integer,
        ForeignKey("coletas.id", name="fk_pesagens_coleta"),
        nullable=False,
    )
    material = Column(String(20), nullable=False)
    quilos = Column(Float, nullable=False)
    pontos = Column(Integer, nullable=False)

    # Esta relação permite localizar a coleta dona da pesagem.
    coleta = relationship("Coleta")
