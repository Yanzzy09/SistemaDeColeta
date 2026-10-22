import repositorios.coleta as repositorio_coleta
import repositorios.pesagem as repositorio_pesagem
import repositorios.usuario as repositorio_usuario
from servicos.excecoes import MoradorInvalido


# Este auxiliar junta o histórico da coleta à resposta para que a moradora possa consultá-lo.
def _com_pesagens(sessao, coleta):
    if coleta is None:
        return None
    return {
        "id": coleta.id,
        "morador_id": coleta.morador_id,
        "morador": coleta.morador.nome,
        "endereco": coleta.endereco,
        "dia": coleta.dia,
        "materiais": [material for material in coleta.materiais.split(",") if material],
        "situacao": coleta.situacao,
        "pontos": coleta.pontos,
        "pesagens": [
            {
                "id": pesagem.id,
                "coleta_id": pesagem.coleta_id,
                "material": pesagem.material,
                "quilos": pesagem.quilos,
                "pontos": pesagem.pontos,
            }
            for pesagem in repositorio_pesagem.listar_pesagens(sessao, coleta.id)
        ],
    }


# Este serviço entrega a lista filtrada sem acrescentar regras além das descritas na cartilha.
def listar_coletas(sessao, dia=None, morador_id=None):
    return [_com_pesagens(sessao, coleta) for coleta in repositorio_coleta.listar_coletas(sessao, dia, morador_id)]


# Este serviço localiza uma coleta para a rota decidir se responde com sucesso ou 404.
def buscar_coleta(sessao, coleta_id):
    return _com_pesagens(sessao, repositorio_coleta.buscar_coleta(sessao, coleta_id))


# Este serviço inicia a coleta no estado agendado e com zero pontos, como determina a cartilha.
def agendar_coleta(sessao, dados, morador_id):
    morador = repositorio_usuario.buscar_usuario(sessao, morador_id)
    if morador is None or morador.tipo != "morador":
        raise MoradorInvalido("A coleta precisa estar ligada a um morador existente.")
    dados_coleta = {
        "morador_id": morador_id,
        "endereco": dados["endereco"],
        "dia": dados["dia"],
        "materiais": ",".join(dados["materiais"]),
        "situacao": "Agendada",
        "pontos": 0,
    }
    return _com_pesagens(sessao, repositorio_coleta.criar_coleta(sessao, dados_coleta))
