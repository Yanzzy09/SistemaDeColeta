import repositorios.usuario as repositorio_usuario
from seguranca import criar_token, gerar_hash, ler_token, verificar_senha
from servicos.excecoes import EmailEmUso


# Este serviço consulta a lista de usuários sem adicionar regras que não estejam na cartilha.
def listar_usuarios(sessao):
    return repositorio_usuario.listar_usuarios(sessao)


# Este serviço busca um usuário para que a rota possa responder sucesso ou 404.
def buscar_usuario(sessao, usuario_id):
    return repositorio_usuario.buscar_usuario(sessao, usuario_id)


# Este serviço encaminha os dados validados para o repositório criar o usuário.
def criar_usuario(sessao, dados):
    if repositorio_usuario.buscar_por_email(sessao, dados["email"]) is not None:
        raise EmailEmUso("Já existe um usuário com esse e-mail.")
    dados_usuario = {
        "nome": dados["nome"],
        "email": dados["email"],
        "tipo": dados["tipo"],
        "senha_hash": gerar_hash(dados["senha"]),
    }
    return repositorio_usuario.criar_usuario(sessao, dados_usuario)


# Este serviço confere e-mail e senha sem revelar qual dos dois dados falhou.
def autenticar(sessao, email, senha):
    usuario = repositorio_usuario.buscar_por_email(sessao, email)
    if usuario is None or usuario.senha_hash is None or not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario


# Este serviço transforma um login válido em um token assinado.
def criar_token_usuario(usuario):
    return criar_token(usuario.id)


# Este serviço traduz o token para o usuário que fez a requisição.
def usuario_do_token(sessao, token):
    usuario_id = ler_token(token)
    if usuario_id is None:
        return None
    return repositorio_usuario.buscar_usuario(sessao, usuario_id)
