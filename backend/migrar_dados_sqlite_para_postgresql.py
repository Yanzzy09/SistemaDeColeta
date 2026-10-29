"""Copia os dados locais do SQLite para o PostgreSQL configurado."""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import configuracao
from banco import Base
from modelos.coleta import Coleta
from modelos.pesagem import Pesagem
from modelos.usuario import Usuario


# A origem continua sendo o banco local legado; o destino usa URL_DO_BANCO.
origem = create_engine("sqlite:///./volta.db")
destino = create_engine(configuracao.URL_DO_BANCO)


def copiar_tabela(modelo):
    """Copia registros de um modelo, preservando seus identificadores."""
    with Session(origem) as sessao_origem, Session(destino) as sessao_destino:
        registros = sessao_origem.scalars(select(modelo)).all()
        for registro in registros:
            sessao_destino.merge(registro)
        sessao_destino.commit()


if __name__ == "__main__":
    Base.metadata.create_all(destino)
    for modelo in (Usuario, Coleta, Pesagem):
        copiar_tabela(modelo)
    print("Dados copiados para o PostgreSQL.")
