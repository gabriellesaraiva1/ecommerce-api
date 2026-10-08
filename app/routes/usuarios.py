from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UsuarioDB
from app.dependencies import get_usuario_atual
from app.security import criar_hash_senha

from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


# ==========================================
# CRIAR USUÁRIO
# ==========================================

@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=201
)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):

    usuario_existente = db.query(UsuarioDB).filter(
        UsuarioDB.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado"
        )

    novo_usuario = UsuarioDB(
        nome=usuario.nome,
        email=usuario.email,
        senha=criar_hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


# ==========================================
# LISTAR USUÁRIOS
# ==========================================

@router.get(
    "/",
    response_model=list[UsuarioResponse]
)
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_atual: UsuarioDB = Depends(get_usuario_atual)
):

    return db.query(UsuarioDB).all()


# ==========================================
# BUSCAR USUÁRIO POR ID
# ==========================================

@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse
)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario


# ==========================================
# ATUALIZAR USUÁRIO
# ==========================================

@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse
)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Session = Depends(get_db)
):

    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if dados.email is not None:

        email_existente = db.query(UsuarioDB).filter(
            UsuarioDB.email == dados.email,
            UsuarioDB.id != usuario_id
        ).first()

        if email_existente:
            raise HTTPException(
                status_code=400,
                detail="E-mail já cadastrado"
            )

    dados_atualizacao = dados.model_dump(
        exclude_unset=True
    )

    # Criptografa a senha caso ela seja alterada
    if "senha" in dados_atualizacao:
        dados_atualizacao["senha"] = criar_hash_senha(
            dados_atualizacao["senha"]
        )

    for campo, valor in dados_atualizacao.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario


# ==========================================
# EXCLUIR USUÁRIO
# ==========================================

@router.delete(
    "/{usuario_id}",
    status_code=204
)
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    db.delete(usuario)
    db.commit()

    return None

