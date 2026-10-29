from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

import configuracao as config
import rotas.coletas as rotas_coletas
import rotas.pesagens as rotas_pesagens
import rotas.usuarios as rotas_usuarios
import rotas.autenticacao as rotas_autenticacao

# Este app reúne as configurações da API e os caminhos definidos nos módulos de rotas.
app = FastAPI(title="Volta — API de Coletas", version="1.0.0")

# O CORS libera somente a origem configurada para o frontend deste ambiente.
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGENS_FRONTEND,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.exception_handler(SQLAlchemyError)
async def erro_de_banco(request: Request, exc: Exception):
    """Retorna uma mensagem acionável quando o banco não aceita a conexão."""
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Banco de dados indisponível. Confira URL_DO_BANCO e a senha do PostgreSQL no arquivo backend/.env."
        },
    )


# Este registro conecta os recursos de coleta e pesagem à aplicação.
app.include_router(rotas_coletas.roteador)
app.include_router(rotas_pesagens.roteador)
app.include_router(rotas_usuarios.roteador)
app.include_router(rotas_autenticacao.roteador)
