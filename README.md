# Volta — sistema de coleta seletiva

Aplicativo para aproximar moradores e cooperativa de reciclagem. A moradora agenda e acompanha coletas; a cooperativa organiza as paradas do dia, registra as pesagens e confere os pontos.

## Frontend

Requer Node.js e npm instalados.

```powershell
cd frontend
npm install
npm run dev
```

Abra o endereço local informado pelo Vite no terminal. Use o seletor no canto superior direito para alternar entre **Moradora** e **Cooperativa**. Os agendamentos e as pesagens ficam salvos no armazenamento local do navegador neste protótipo.

Para gerar a versão de produção, dentro de `frontend/`, execute `npm run build`.

## Backend

O backend usa FastAPI, SQLAlchemy e MySQL. O Alembic registra as mudanças das tabelas em `backend/migracoes/`.

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copie `.env.exemplo` para `.env` e preencha `URL_DO_BANCO` com o endereço do seu MySQL. Depois, crie as tabelas do banco vazio:

```powershell
python criar_tabelas.py
alembic stamp head
```

Para uma alteração posterior nos modelos:

```powershell
alembic revision --autogenerate -m "descreva a mudança"
alembic upgrade head
```

Para subir a API (o SQLite local já é configurado no `.env`):

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Com o servidor ativo, abra `http://127.0.0.1:8000/docs`. As rotas principais são:

| Método | Caminho | Finalidade |
| --- | --- | --- |
| POST | `/usuarios` | Cadastra nome, e-mail, senha e perfil |
| GET | `/usuarios/eu` | Mostra o usuário do token atual |
| POST | `/login` | Confere e-mail e senha e devolve JWT |
| GET | `/coletas` | Lista coletas, com filtros por dia e morador |
| POST | `/coletas` | Agenda uma coleta |
| GET | `/coletas/{id}` | Consulta uma coleta e seu histórico |
| GET | `/coletas/{id}/pesagens` | Lista as pesagens |
| POST | `/coletas/{id}/pesagens` | Registra uma pesagem e soma os pontos |

Antes do primeiro login, cadastre os dois perfis pelo `POST /usuarios`: Joana com tipo `morador` e Osmar com tipo `cooperativa`. A senha deve ter entre 8 e 72 caracteres.

A API usa Argon2 para guardar apenas o hash da senha e JWT para identificar a sessão. O login recebe formulário com `username` (e-mail) e `password`, devolve um token Bearer e o frontend guarda esse token no `localStorage`.

As rotas de coleta exigem autenticação. A moradora vê e agenda somente as próprias coletas; a cooperativa vê a rota e registra pesagens. Sem token, a API responde 401. Com token válido, mas perfil inadequado, responde 403. O cadastro de e-mail repetido responde 409.
