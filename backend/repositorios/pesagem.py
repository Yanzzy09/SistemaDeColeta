from sqlalchemy import select

from modelos.pesagem import Pesagem


# Este repositório devolve as pesagens que pertencem à coleta consultada.
def listar_pesagens(sessao, coleta_id):
    consulta = select(Pesagem).where(Pesagem.coleta_id == coleta_id).order_by(Pesagem.id)
    return sessao.scalars(consulta).all()


# Este repositório salva uma pesagem e atribui a ela um identificador sequencial.
def criar_pesagem(sessao, dados):
    nova_pesagem = Pesagem(**dados)
    sessao.add(nova_pesagem)
    sessao.flush()
    return nova_pesagem
