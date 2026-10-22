from fastapi import APIRouter, Depends, HTTPException, status

from banco import obter_sessao
import servicos.usuario as servico_usuario
from rotas.autenticacao import obter_usuario_atual
from servicos.excecoes import EmailEmUso
from esquemas.usuario import UsuarioEntrada, UsuarioResposta

# Este roteador reúne os caminhos de consulta e criação de usuários.
roteador = APIRouter(prefix="/usuarios", tags=["Usuários"])


# Esta rota lista os usuários cadastrados para apoiar a escolha de perfil na aplicação.
@roteador.get("", response_model=list[UsuarioResposta], summary="Listar usuários")
def listar_usuarios(sessao=Depends(obter_sessao), usuario=Depends(obter_usuario_atual)):
    """Lista os usuários disponíveis para a escolha de perfil."""
    return servico_usuario.listar_usuarios(sessao)


# Esta rota devolve os dados públicos do usuário identificado pelo token, sem senha ou hash.
@roteador.get("/eu", response_model=UsuarioResposta, summary="Consultar meu usuário", responses={401: {"description": "Token ausente ou inválido."}})
def consultar_usuario_atual(usuario=Depends(obter_usuario_atual)):
    """Mostra o perfil associado ao token atual."""
    return usuario


# Esta rota mostra um usuário específico ou informa que ele não existe.
@roteador.get(
    "/{usuario_id}",
    response_model=UsuarioResposta,
    summary="Consultar um usuário",
    responses={404: {"description": "O usuário não foi encontrado."}},
)
def buscar_usuario(usuario_id: int, sessao=Depends(obter_sessao)):
    """Busca um usuário pelo identificador."""
    usuario = servico_usuario.buscar_usuario(sessao, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return usuario


# Esta rota cria um usuário com os dados validados pelo esquema de entrada.
@roteador.post(
    "",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um usuário",
    responses={409: {"description": "O e-mail já está cadastrado."}},
)
def criar_usuario(dados: UsuarioEntrada, sessao=Depends(obter_sessao)):
    """Cria um usuário com nome e perfil morador ou cooperativa."""
    try:
        return servico_usuario.criar_usuario(sessao, dados.model_dump())
    except EmailEmUso as erro:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro))
