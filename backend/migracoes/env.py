from logging.config import fileConfig

from alembic import context

from banco import Base, engine
from modelos import coleta, pesagem, usuario
import configuracao as configuracao_projeto

config = context.config

# Este bloco mantém os logs do Alembic legíveis durante a criação da migration.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Esta metadata reúne os três modelos e permite ao autogenerate comparar o banco com o código.
target_metadata = Base.metadata


# Esta função prepara uma migration sem abrir uma conexão com o banco.
def run_migrations_offline() -> None:
    url = configuracao_projeto.URL_DO_BANCO
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Esta função aplica ou gera migrations usando o engine configurado no backend.
def run_migrations_online() -> None:
    with engine.connect() as conexao:
        context.configure(connection=conexao, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
