from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UsuarioDB


SECRET_KEY = "chave-secreta-do-ecommerce"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise credenciais_invalidas

        usuario_id = int(usuario_id)

    except (JWTError, ValueError):
        raise credenciais_invalidas

    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()

    if usuario is None:
        raise credenciais_invalidas

    if not usuario.ativo:
        raise HTTPException(
            status_code=403,
            detail="Usuário inativo"
        )

    return usuario