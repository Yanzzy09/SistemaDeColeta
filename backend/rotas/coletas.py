from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status

from banco import obter_sessao
import servicos.coleta as servico_coleta
from rotas.autenticacao import exigir_morador, obter_usuario_atual
from esquemas.coleta import ColetaEntrada, ColetaResposta

# Este roteador agrupa os caminhos de consulta e agendamento que a moradora usa.
roteador = APIRouter(prefix="/coletas", tags=["Coletas"])


# Esta rota permite que a moradora consulte suas coletas e que a cooperativa filtre a rota por dia ou morador.
@roteador.get(
    "",
    response_model=list[ColetaResposta],
    summary="Listar coletas",
    responses={401: {"description": "Token ausente ou inválido."}},
)
def listar_coletas(
    dia: date | None = Query(default=None, description="Filtra as coletas por dia"),
    morador_id: int | None = Query(default=None, gt=0, description="Filtra pelo identificador do morador"),
    sessao=Depends(obter_sessao),
    usuario=Depends(obter_usuario_atual),
):
    """Lista as coletas por dia e, quando informado, pelo morador responsável."""
    filtro_morador = usuario.id if usuario.tipo == "morador" else morador_id
    return servico_coleta.listar_coletas(sessao, dia, filtro_morador)


# Esta rota mostra os dados e o total de pontos de uma coleta específica.
@roteador.get(
    "/{coleta_id}",
    response_model=ColetaResposta,
    summary="Consultar uma coleta",
    responses={404: {"description": "A coleta não foi encontrada."}, 401: {"description": "Token ausente ou inválido."}, 403: {"description": "A coleta pertence a outro morador."}},
)
def buscar_coleta(coleta_id: int, sessao=Depends(obter_sessao), usuario=Depends(obter_usuario_atual)):
    """Mostra uma coleta, seus materiais, status, pontos e histórico de pesagens."""
    coleta = servico_coleta.buscar_coleta(sessao, coleta_id)
    if coleta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coleta não encontrada.")
    if usuario.tipo == "morador" and coleta["morador_id"] != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Esta coleta não é sua.")
    return coleta


# Esta rota recebe os dados do agendamento e devolve a coleta criada com status 201.
@roteador.post(
    "",
    response_model=ColetaResposta,
    status_code=status.HTTP_201_CREATED,
    summary="Agendar uma coleta",
    responses={403: {"description": "A cooperativa não pode agendar coleta."}},
)
def agendar_coleta(dados: ColetaEntrada, sessao=Depends(obter_sessao), usuario=Depends(exigir_morador)):
    """Cria uma coleta com situação agendada e zero pontos."""
    return servico_coleta.agendar_coleta(sessao, dados.model_dump(), usuario.id)
