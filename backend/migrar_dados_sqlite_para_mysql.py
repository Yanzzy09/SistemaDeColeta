"""Copia os dados locais para o MySQL depois da migration do schema."""

from sqlalchemy import create_engine, text

import configuracao


# NOVO: a migration cria a estrutura; este script preserva os dados do protótipo.
origem = create_engine("sqlite:///./volta.db")
destino = create_engine(configuracao.URL_DO_BANCO)

with origem.connect() as conexao_origem, destino.begin() as conexao_destino:
    # NOVO: a ordem respeita as chaves estrangeiras entre usuários, coletas e pesagens.
    tabelas = {
        "usuarios": ["id", "nome", "tipo", "email", "senha_hash"],
        "coletas": ["id", "morador_id", "endereco", "dia", "materiais", "situacao", "pontos"],
        "pesagens": ["id", "coleta_id", "material", "quilos", "pontos"],
    }
    for tabela, colunas in tabelas.items():
        linhas = conexao_origem.execute(text(f"SELECT {', '.join(colunas)} FROM {tabela}")).mappings().all()
        if not linhas:
            continue
        quantidade = conexao_destino.execute(text(f"SELECT COUNT(*) FROM {tabela}")).scalar_one()
        if quantidade:
            print(f"{tabela}: já possui dados; ignorando cópia")
            continue
        nomes = ", ".join(colunas)
        valores = ", ".join(f":{coluna}" for coluna in colunas)
        conexao_destino.execute(text(f"INSERT INTO {tabela} ({nomes}) VALUES ({valores})"), linhas)
        print(f"{tabela}: {len(linhas)} registro(s) copiado(s)")

