# Esta exceção identifica uma requisição que aponta para um morador inexistente.
class MoradorInvalido(Exception):
    pass


# Esta exceção informa que o e-mail já pertence a outro usuário.
class EmailEmUso(Exception):
    pass
