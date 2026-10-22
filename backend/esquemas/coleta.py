from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Estes tipos limitam os valores às opções da cartilha e aos dois estados previstos para a coleta.
TipoMaterial = Literal["Papel", "Vidro", "Plástico", "Metal"]
SituacaoColeta = Literal["Agendada", "Coletada"]


# Este esquema valida os dados que a moradora precisa informar para agendar uma coleta.
class ColetaEntrada(BaseModel):
    endereco: str = Field(min_length=5, description="Endereço onde o material será recolhido", examples=["Rua das Palmeiras, 128"])
    dia: date = Field(description="Dia escolhido para a coleta", examples=["2026-10-10"])
    materiais: list[TipoMaterial] = Field(min_length=1, description="Materiais separados para a coleta", examples=[["Papel", "Plástico"]])


# Este esquema descreve os dados da coleta que as telas podem consultar.
class ColetaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    morador_id: int
    morador: str
    endereco: str
    dia: date
    materiais: list[TipoMaterial]
    situacao: SituacaoColeta
    pontos: float
    pesagens: list[dict] = Field(default_factory=list)
