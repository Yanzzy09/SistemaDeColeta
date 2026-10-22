from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Este tipo limita o perfil às duas pessoas previstas na cartilha, sem criar login ou senha.
TipoUsuario = Literal["morador", "cooperativa"]


# NOVO: estes valores representam os grupos de autorização das duas personas.
# O campo `tipo` da tabela permanece compatível com os dados já existentes.
class GrupoUsuario(str, Enum):
    MORADOR = "morador"
    COOPERATIVA = "cooperativa"


# Este esquema valida os dados básicos usados quando um usuário é informado ao sistema.
class UsuarioEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=100, description="Nome da pessoa que usa o sistema", examples=["Joana Martins"])
    email: str = Field(min_length=5, max_length=100, description="E-mail usado no login", examples=["joana@volta.com"])
    senha: str = Field(min_length=8, max_length=72, description="Senha usada no login", examples=["separa2026"])
    tipo: TipoUsuario = Field(description="Perfil escolhido na tela: morador ou cooperativa", examples=["morador"])


# Este esquema representa um usuário identificado quando ele é devolvido pela API.
class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str | None
    tipo: TipoUsuario


# Este esquema representa a resposta do login sem expor senha ou hash.
class Token(BaseModel):
    access_token: str
    token_type: str


# NOVO: formato da resposta que informa ao frontend as ações do grupo atual.
class PermissoesResposta(BaseModel):
    grupo: TipoUsuario
    permissoes: list[str]
