from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EnderecoDB
from app.dependencies import get_usuario_atual

from app.schemas.endereco import (
    EnderecoCreate,
    EnderecoResponse
)


router = APIRouter(
    prefix="/enderecos",
    tags=["Endereços"]
)


# ==========================================================
# CRIAR ENDEREÇO
# ==========================================================

@router.post(
    "/",
    response_model=EnderecoResponse,
    status_code=201
)
def criar_endereco(
    endereco: EnderecoCreate,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_usuario_atual)
):

    novo_endereco = EnderecoDB(
        usuario_id=usuario_atual.id,
        cep=endereco.cep,
        rua=endereco.rua,
        numero=endereco.numero,
        complemento=endereco.complemento,
        bairro=endereco.bairro,
        cidade=endereco.cidade,
        estado=endereco.estado
    )

    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)

    return novo_endereco