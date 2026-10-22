from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Este tipo restringe a pesagem aos materiais cuja pontuação está definida na cartilha.
TipoMaterial = Literal["Papel", "Vidro", "Plástico", "Metal"]


# Este esquema aceita somente materiais previstos e pesos positivos informados pela cooperativa.
class PesagemEntrada(BaseModel):
    material: TipoMaterial = Field(examples=["Metal"])
    quilos: float = Field(gt=0, description="Peso do material em quilos", examples=[2.0])


# Este esquema apresenta o cálculo de pontos feito no serviço para cada pesagem registrada.
class PesagemResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    coleta_id: int
    material: TipoMaterial
    quilos: float
    pontos: float
