from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

import configuracao as config

# Este hasher usa Argon2 para guardar somente uma digital lenta e salgada da senha.
hasher = PasswordHash.recommended()


# Esta função transforma a senha recebida no cadastro em um hash que não pode ser revertido.
def gerar_hash(senha: str):
    return hasher.hash(senha)


# Esta função compara a senha informada no login com o hash salvo no banco.
def verificar_senha(senha: str, senha_hash: str):
    return hasher.verify(senha, senha_hash)


# Esta função cria um token assinado com o id do usuário e uma validade de uma hora.
def criar_token(usuario_id: int):
    expiracao = datetime.now(timezone.utc) + timedelta(hours=1)
    dados = {"sub": str(usuario_id), "exp": expiracao}
    return jwt.encode(dados, config.CHAVE_DO_TOKEN, algorithm="HS256")


# Esta função valida o token e devolve o id do usuário ou None quando ele não é confiável.
def ler_token(token: str):
    try:
        dados = jwt.decode(token, config.CHAVE_DO_TOKEN, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    return int(dados["sub"])
