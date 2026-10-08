from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CategoriaDB
from app.dependencies import get_usuario_atual
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate
)


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=201
)
def criar_categoria(
categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario_atual = Depends(get_usuario_atual)
):
    categoria_existente = db.query(CategoriaDB).filter(
        CategoriaDB.nome == categoria.nome
    ).first()

    if categoria_existente:
        raise HTTPException(
            status_code=400,
            detail="Categoria já cadastrada"
        )

    nova_categoria = CategoriaDB(
        nome=categoria.nome,
        descricao=categoria.descricao
    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


@router.get(
    "/",
    response_model=list[CategoriaResponse]
)
def listar_categorias(
    db: Session = Depends(get_db)
):
    return db.query(CategoriaDB).all()


@router.get(
    "/{categoria_id}",
    response_model=CategoriaResponse
)
def buscar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    categoria = db.query(CategoriaDB).filter(
        CategoriaDB.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return categoria


@router.put(
    "/{categoria_id}",
    response_model=CategoriaResponse
)
def atualizar_categoria(
    categoria_id: int,
    dados: CategoriaUpdate,
    db: Session = Depends(get_db),
    usuario_atual = Depends(get_usuario_atual)
):
    categoria = db.query(CategoriaDB).filter(
        CategoriaDB.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    dados_atualizacao = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in dados_atualizacao.items():
        setattr(categoria, campo, valor)

    db.commit()
    db.refresh(categoria)

    return categoria


@router.delete(
    "/{categoria_id}",
    status_code=204
)
def excluir_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario_atual = Depends(get_usuario_atual)
):
    categoria = db.query(CategoriaDB).filter(
        CategoriaDB.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    db.delete(categoria)
    db.commit()

    return None