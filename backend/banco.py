from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import configuracao as config

# Este engine representa a conexão configurada para o MySQL sem abrir uma sessão por conta própria.
opcoes_engine = {"pool_pre_ping": True}
if config.URL_DO_BANCO.startswith("sqlite"):
    opcoes_engine["connect_args"] = {"check_same_thread": False}
engine = create_engine(config.URL_DO_BANCO, **opcoes_engine)

# Esta fábrica cria uma sessão independente para cada requisição da API.
Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Esta classe é a base que reúne os metadados das três tabelas do projeto.
class Base(DeclarativeBase):
    pass


# Esta dependência entrega uma sessão à rota e a fecha quando a requisição termina.
def obter_sessao():
    with Sessao() as sessao:
        yield sessao
