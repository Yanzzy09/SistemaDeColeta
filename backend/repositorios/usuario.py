from sqlalchemy import select

from modelos.usuario import Usuario


# Este repositório devolve todos os usuários cadastrados para a consulta da cooperativa.
def listar_usuarios(sessao):
    return sessao.scalars(select(Usuario).order_by(Usuario.id)).all()


# Este repositório procura um usuário pelo identificador informado.
def buscar_usuario(sessao, usuario_id):
    return sessao.get(Usuario, usuario_id)


# Este repositório localiza o usuário pelo e-mail informado no login ou cadastro.
def buscar_por_email(sessao, email):
    consulta = select(Usuario).where(Usuario.email == email)
    return sessao.scalars(consulta).first()


# Este repositório grava um novo usuário e atribui um identificador sequencial.
def criar_usuario(sessao, dados):
    novo_usuario = Usuario(**dados)
    sessao.add(novo_usuario)
    sessao.commit()
    sessao.refresh(novo_usuario)
    return novo_usuario
