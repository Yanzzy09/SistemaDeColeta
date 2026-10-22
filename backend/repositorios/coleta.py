from sqlalchemy import select

from modelos.coleta import Coleta


# Repositório que consulta as coletas e aplica os filtros opcionais da rota.
def listar_coletas(sessao, dia=None, morador_id=None):
    consulta = select(Coleta).order_by(Coleta.dia, Coleta.id)
    if dia is not None:
        consulta = consulta.where(Coleta.dia == dia)
    if morador_id is not None:
        consulta = consulta.where(Coleta.morador_id == morador_id)
    return sessao.scalars(consulta).all()


# Repositório que busca uma coleta pelo identificador.
def buscar_coleta(sessao, coleta_id):
    return sessao.get(Coleta, coleta_id)


# Repositório que grava uma coleta nova no banco.
def criar_coleta(sessao, dados):
    nova_coleta = Coleta(**dados)
    sessao.add(nova_coleta)
    sessao.commit()
    sessao.refresh(nova_coleta)
    return nova_coleta


# Repositório que atualiza pontos e situação após uma pesagem.
def atualizar_coleta(sessao, coleta, pontos, situacao):
    coleta.pontos = pontos
    coleta.situacao = situacao
    sessao.commit()
    sessao.refresh(coleta)
    return coleta
