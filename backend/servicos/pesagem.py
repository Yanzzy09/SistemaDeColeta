import repositorios.coleta as repositorio_coleta
import repositorios.pesagem as repositorio_pesagem

# A regra atual é igual para todos os materiais: um ponto a cada dois quilos completos.
QUILOS_POR_PONTO = 2


# Este serviço devolve as pesagens da coleta ou None quando a coleta não existe.
def listar_pesagens(sessao, coleta_id):
    coleta = repositorio_coleta.buscar_coleta(sessao, coleta_id)
    if coleta is None:
        return None
    return repositorio_pesagem.listar_pesagens(sessao, coleta_id)


# Este serviço calcula pontos, salva a pesagem, soma o total e muda a situação para coletada.
def registrar_pesagem(sessao, coleta_id, dados):
    coleta = repositorio_coleta.buscar_coleta(sessao, coleta_id)
    if coleta is None:
        return None

    pontos = int(dados["quilos"] // QUILOS_POR_PONTO)
    dados_pesagem = {
        **dados,
        "coleta_id": coleta_id,
        "pontos": pontos,
    }
    pesagem = repositorio_pesagem.criar_pesagem(sessao, dados_pesagem)
    repositorio_coleta.atualizar_coleta(sessao, coleta, coleta.pontos + pontos, "Coletada")
    return pesagem
