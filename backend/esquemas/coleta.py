from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Estes tipos limitam os valores às opções da cartilha e aos dois estados previstos para a coleta.
TipoMaterial = Literal["Papel", "Vidro", "Plástico", "Metal"]
SituacaoColeta = Literal["Agendada", "Coletada"]


# Este esquema valida os dados que a moradora precisa informar para marcar uma coleta.
class ColetaEntrada(BaseModel):
    endereco: str = Field(min_length=5, description="Endereço onde o material será recolhido")
    dia: date = Field(description="Dia escolhido para a coleta")
    materiais: list[TipoMaterial] = Field(min_length=1, description="Materiais separados para a coleta")
    descricao: str = Field(default="", max_length=500, description="Objetos e detalhes da coleta")


# Este esquema descreve os dados da coleta que as telas podem consultar.
class ColetaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    morador_id: int
    morador: str
    endereco: str
    dia: date
    materiais: list[TipoMaterial]
    descricao: str
    situacao: SituacaoColeta
    pontos: float
    pesagens: list[dict] = Field(default_factory=list)
