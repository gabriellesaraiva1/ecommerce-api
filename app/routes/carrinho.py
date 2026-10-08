from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    CarrinhoDB,
    CarrinhoItemDB,
    ProdutoDB
)

from app.dependencies import get_usuario_atual


router = APIRouter(
    prefix="/carrinho",
    tags=["Carrinho"]
)


# ==========================================================
# CRIAR CARRINHO
# ==========================================================

@router.post("/")
def criar_carrinho(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_usuario_atual)
):

    carrinho_existente = db.query(CarrinhoDB).filter(
        CarrinhoDB.usuario_id == usuario_atual.id
    ).first()

    if carrinho_existente:
        raise HTTPException(
            status_code=400,
            detail="Usuário já possui um carrinho"
        )

    novo_carrinho = CarrinhoDB(
        usuario_id=usuario_atual.id
    )

    db.add(novo_carrinho)
    db.commit()
    db.refresh(novo_carrinho)

    return {
        "mensagem": "Carrinho criado com sucesso",
        "id": novo_carrinho.id,
        "usuario_id": novo_carrinho.usuario_id,
        "data_criacao": novo_carrinho.data_criacao
    }


# ==========================================================
# ADICIONAR PRODUTO AO CARRINHO
# ==========================================================

@router.post("/adicionar")
def adicionar_produto(
    produto_id: int,
    quantidade: int = 1,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_usuario_atual)
):

    if quantidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="A quantidade deve ser maior que zero"
        )

    carrinho = db.query(CarrinhoDB).filter(
        CarrinhoDB.usuario_id == usuario_atual.id
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado"
        )

    produto = db.query(ProdutoDB).filter(
        ProdutoDB.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    if not produto.ativo:
        raise HTTPException(
            status_code=400,
            detail="Produto está inativo"
        )

    if produto.estoque < quantidade:
        raise HTTPException(
            status_code=400,
            detail="Quantidade solicitada maior que o estoque disponível"
        )

    item_existente = db.query(CarrinhoItemDB).filter(
        CarrinhoItemDB.carrinho_id == carrinho.id,
        CarrinhoItemDB.produto_id == produto_id
    ).first()

    if item_existente:

        nova_quantidade = item_existente.quantidade + quantidade

        if nova_quantidade > produto.estoque:
            raise HTTPException(
                status_code=400,
                detail="Quantidade total maior que o estoque disponível"
            )

        item_existente.quantidade = nova_quantidade

    else:

        novo_item = CarrinhoItemDB(
            carrinho_id=carrinho.id,
            produto_id=produto_id,
            quantidade=quantidade
        )

        db.add(novo_item)

    db.commit()

    return {
        "mensagem": "Produto adicionado ao carrinho",
        "produto_id": produto_id,
        "quantidade": quantidade
    }


# ==========================================================
# REMOVER PRODUTO DO CARRINHO
# ==========================================================

@router.delete("/remover/{produto_id}")
def remover_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_usuario_atual)
):

    carrinho = db.query(CarrinhoDB).filter(
        CarrinhoDB.usuario_id == usuario_atual.id
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado"
        )

    item = db.query(CarrinhoItemDB).filter(
        CarrinhoItemDB.carrinho_id == carrinho.id,
        CarrinhoItemDB.produto_id == produto_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado no carrinho"
        )

    db.delete(item)
    db.commit()

    return {
        "mensagem": "Produto removido do carrinho",
        "produto_id": produto_id
    }


# ==========================================================
# ALTERAR QUANTIDADE
# ==========================================================

@router.put("/quantidade/{produto_id}")
def alterar_quantidade(
    produto_id: int,
    quantidade: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_usuario_atual)
):

    if quantidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="A quantidade deve ser maior que zero"
        )

    carrinho = db.query(CarrinhoDB).filter(
        CarrinhoDB.usuario_id == usuario_atual.id
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado"
        )

    item = db.query(CarrinhoItemDB).filter(
        CarrinhoItemDB.carrinho_id == carrinho.id,
        CarrinhoItemDB.produto_id == produto_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado no carrinho"
        )

    produto = db.query(ProdutoDB).filter(
        ProdutoDB.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    if not produto.ativo:
        raise HTTPException(
            status_code=400,
            detail="Produto está inativo"
        )

    if quantidade > produto.estoque:
        raise HTTPException(
            status_code=400,
            detail="Quantidade maior que o estoque disponível"
        )

    item.quantidade = quantidade

    db.commit()
    db.refresh(item)

    return {
        "mensagem": "Quantidade alterada com sucesso",
        "produto_id": produto_id,
        "quantidade": item.quantidade
    }


# ==========================================================
# VISUALIZAR CARRINHO
# ==========================================================

@router.get("/")
def visualizar_carrinho(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_usuario_atual)
):

    carrinho = db.query(CarrinhoDB).filter(
        CarrinhoDB.usuario_id == usuario_atual.id
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado"
        )

    itens = []

    total = 0

    for item in carrinho.itens:

        produto = item.produto

        subtotal = produto.preco * item.quantidade

        total += subtotal

        itens.append({
            "produto_id": produto.id,
            "produto": produto.nome,
            "preco_unitario": produto.preco,
            "quantidade": item.quantidade,
            "subtotal": subtotal
        })

    return {
        "carrinho_id": carrinho.id,
        "usuario_id": carrinho.usuario_id,
        "itens": itens,
        "total": total
    }