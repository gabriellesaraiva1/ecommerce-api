import bcrypt


def criar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")

    hash_senha = bcrypt.hashpw(
        senha_bytes,
        bcrypt.gensalt()
    )

    return hash_senha.decode("utf-8")


def verificar_senha(
    senha: str,
    hash_senha: str
) -> bool:

    return bcrypt.checkpw(
        senha.encode("utf-8"),
        hash_senha.encode("utf-8")
    )