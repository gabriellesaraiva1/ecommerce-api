from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ProdutoDB, CategoriaDB
from app.dependencies import get_usuario_atual
from app.schemas.produto import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoUpdate
)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


# ==========================================
# CRIAR PRODUTO
# ==========================================

@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_atual = Depends(get_usuario_atual)
):

    if produto.categoria_id is not None:

        categoria = db.query(CategoriaDB).filter(
            CategoriaDB.id == produto.categoria_id
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=404,
                detail="Categoria não encontrada"
            )

    novo_produto = ProdutoDB(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        estoque=produto.estoque,
        categoria_id=produto.categoria_id
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


# ==========================================
# LISTAR PRODUTOS
# ==========================================

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(
    db: Session = Depends(get_db)
):

    produtos = db.query(ProdutoDB).all()

    return produtos


# ==========================================
# BUSCAR PRODUTO POR ID
# ==========================================

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):

    produto = db.query(ProdutoDB).filter(
        ProdutoDB.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto


# ==========================================
# ATUALIZAR PRODUTO
# ==========================================

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db),
    usuario_atual = Depends(get_usuario_atual)
):

    produto = db.query(ProdutoDB).filter(
        ProdutoDB.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    # Verifica categoria, caso tenha sido informada
    if dados.categoria_id is not None:

        categoria = db.query(CategoriaDB).filter(
            CategoriaDB.id == dados.categoria_id
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
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto


# ==========================================
# EXCLUIR PRODUTO
# ==========================================

@router.delete("/{produto_id}", status_code=204)
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_atual = Depends(get_usuario_atual)
):

    produto = db.query(ProdutoDB).filter(
        ProdutoDB.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()

    return None