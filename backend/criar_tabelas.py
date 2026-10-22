from banco import Base, engine
from modelos import coleta, pesagem, usuario

# Este comando importa os três modelos e cria as tabelas que ainda não existem no banco vazio.
Base.metadata.create_all(engine)
