from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from banco import obter_sessao
import servicos.usuario as servico_usuario
from esquemas.usuario import GrupoUsuario, PermissoesResposta, Token

# Este esquema procura o token Bearer no cabeçalho das rotas protegidas.
esquema_oauth = OAuth2PasswordBearer(tokenUrl="login")

# Este roteador concentra o login e as dependências de autenticação e perfil.
roteador = APIRouter(tags=["Autenticação"])


# NOVO: mapa central dos grupos e das permissões do sistema.
# Ele serve como documentação executável: toda rota protegida deve usar uma
# dependência que confira um dos grupos listados aqui.
PERMISSOES_POR_GRUPO = {
    GrupoUsuario.MORADOR.value: [
        "consultar o próprio perfil",
        "listar e consultar as próprias coletas",
        "agendar coleta",
        "consultar as pesagens das próprias coletas",
    ],
    GrupoUsuario.COOPERATIVA.value: [
        "consultar o próprio perfil",
        "listar coletas e filtrar a rota",
        "consultar coletas de moradores",
        "consultar pesagens",
        "registrar pesagem",
    ],
}


# Esta rota valida o formulário de login e entrega o token que identifica o usuário.
@roteador.post("/login", response_model=Token, summary="Entrar no sistema")
def login(formulario: OAuth2PasswordRequestForm = Depends(), sessao=Depends(obter_sessao)):
    """Confere e-mail e senha e devolve um token Bearer para as próximas requisições."""
    usuario = servico_usuario.autenticar(sessao, formulario.username, formulario.password)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": servico_usuario.criar_token_usuario(usuario), "token_type": "bearer"}


# Esta dependência transforma o token válido no usuário atual da requisição.
def obter_usuario_atual(token: str = Depends(esquema_oauth), sessao=Depends(obter_sessao)):
    usuario = servico_usuario.usuario_do_token(sessao, token)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou vencido.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario


# NOVO: dependência genérica para proteger uma rota com um ou mais grupos.
# O FastAPI executa esta função antes da rota; grupo incompatível recebe 403.
def exigir_grupos(*grupos: GrupoUsuario):
    grupos_permitidos = {grupo.value for grupo in grupos}

    def dependencia(usuario=Depends(obter_usuario_atual)):
        if usuario.tipo not in grupos_permitidos:
            nomes = ", ".join(sorted(grupos_permitidos))
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Esta rota exige um grupo autorizado: {nomes}.",
            )
        return usuario

    return dependencia


# Esta dependência libera as rotas próprias da moradora e bloqueia os outros perfis com 403.
def exigir_morador(usuario=Depends(obter_usuario_atual)):
    return exigir_grupos(GrupoUsuario.MORADOR)(usuario)


# Esta dependência libera as rotas operacionais da cooperativa e bloqueia os outros perfis com 403.
def exigir_cooperativa(usuario=Depends(obter_usuario_atual)):
    return exigir_grupos(GrupoUsuario.COOPERATIVA)(usuario)


# NOVO: endpoint para o frontend saber quais ações o grupo autenticado pode executar.
@roteador.get("/permissoes", response_model=PermissoesResposta, summary="Listar permissões do grupo atual")
def listar_permissoes(usuario=Depends(obter_usuario_atual)):
    return {
        "grupo": usuario.tipo,
        "permissoes": PERMISSOES_POR_GRUPO.get(usuario.tipo, []),
    }
