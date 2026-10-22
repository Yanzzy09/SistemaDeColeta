# Regras do projeto para a IA

Atualizado até a aula 8 da UC4.

## Estrutura

- A raiz contém `docs/`, `frontend/`, `backend/` e `README.md`.
- O backend usa FastAPI, SQLAlchemy, MySQL e Alembic.
- `configuracao.py` é o único arquivo que lê o `.env`.
- `banco.py` contém `engine`, `Sessao`, `Base` e `obter_sessao`.
- `modelos/` contém os modelos SQLAlchemy; `esquemas/` contém os esquemas Pydantic.
- A chamada segue sempre `rota → serviço → repositório`.
- O repositório recebe a sessão como primeiro parâmetro e é o único que usa os modelos e a sessão.
- A sessão chega à rota por `Depends(obter_sessao)`.
- Mudanças de tabelas existentes são registradas em `migracoes/` com Alembic.

## Segurança

- Usuários têm nome, tipo, e-mail e `senha_hash`.
- A senha nunca é salva, devolvida, registrada em log ou colocada no token.
- O hash usa `pwdlib` com Argon2.
- O login usa formulário OAuth2 e devolve JWT assinado com `CHAVE_DO_TOKEN` do `.env`.
- O dono de uma coleta vem do token, nunca do corpo da requisição.
- `401` significa token ausente, inválido ou vencido.
- `403` significa perfil autenticado sem permissão ou registro de outro usuário.
- A moradora vê e agenda somente suas coletas.
- A cooperativa consulta a rota e registra pesagens.

## Código

- Use `def`, nunca `async def`.
- Código, comentários, nomes e respostas ficam em português do Brasil.
- Toda rota, função ou bloco novo recebe comentário curto explicando sua intenção.
- O serviço não importa `HTTPException`; exceções de negócio ficam em `servicos/excecoes.py`.
- A rota ou o `main.py` traduz exceções de negócio para status HTTP.
- Não use banco SQLite, ORM diferente, `pydantic-settings`, `passlib`, `bcrypt` direto, MD5, SHA-256, refresh token, cookies, OAuth externo ou tabela de permissões.
- O frontend usa React, `fetch`, `URLSearchParams` no login e `localStorage` somente para o token.
