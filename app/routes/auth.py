from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models import UsuarioDB
from fastapi.security import OAuth2PasswordRequestForm
from app.security import verificar_senha
from jose import jwt


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


SECRET_KEY = "chave-secreta-do-ecommerce"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post("/login")
def login(
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.email == dados.username
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )

    senha_correta = verificar_senha(
        dados.password,
        usuario.senha
    )

    if not senha_correta:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos"
        )

    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(usuario.id),
        "email": usuario.email,
        "exp": expiracao
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }