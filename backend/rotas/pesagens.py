from fastapi import APIRouter, Depends, HTTPException, status

from banco import obter_sessao
import servicos.pesagem as servico_pesagem
from esquemas.pesagem import PesagemEntrada, PesagemResposta
from rotas.autenticacao import exigir_cooperativa, obter_usuario_atual
import servicos.coleta as servico_coleta

# Este roteador agrupa a consulta e o registro das pesagens feitas pela cooperativa.
roteador = APIRouter(prefix="/coletas/{coleta_id}/pesagens", tags=["Pesagens"])


# Esta rota devolve os materiais pesados daquela coleta, incluindo os pontos de cada pesagem.
@roteador.get(
    "",
    response_model=list[PesagemResposta],
    summary="Listar pesagens",
    responses={404: {"description": "A coleta não foi encontrada."}, 401: {"description": "Token ausente ou inválido."}, 403: {"description": "A coleta pertence a outro morador."}},
)
def listar_pesagens(coleta_id: int, sessao=Depends(obter_sessao), usuario=Depends(obter_usuario_atual)):
    """Lista os materiais pesados e os pontos de uma coleta."""
    pesagens = servico_pesagem.listar_pesagens(sessao, coleta_id)
    if pesagens is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coleta não encontrada.")
    if usuario.tipo == "morador":
        coleta = servico_coleta.buscar_coleta(sessao, coleta_id)
        if coleta["morador_id"] != usuario.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Esta coleta não é sua.")
    return pesagens


# Esta rota registra uma pesagem e responde com os pontos calculados pelo serviço.
@roteador.post(
    "",
    response_model=PesagemResposta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar uma pesagem",
    responses={404: {"description": "A coleta informada não existe."}, 403: {"description": "Apenas a cooperativa registra pesagens."}},
)
def registrar_pesagem(coleta_id: int, dados: PesagemEntrada, sessao=Depends(obter_sessao), usuario=Depends(exigir_cooperativa)):
    """Registra o peso, calcula os pontos e atualiza o total da coleta."""
    pesagem = servico_pesagem.registrar_pesagem(sessao, coleta_id, dados.model_dump())
    if pesagem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coleta não encontrada.")
    return pesagem
