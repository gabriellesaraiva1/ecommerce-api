from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    PedidoDB,
    PedidoItemDB,
    ProdutoDB,
    UsuarioDB,
    EnderecoDB,
    CarrinhoDB,
    CarrinhoItemDB
)

from app.dependencies import get_usuario_atual


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


# ==========================================================
# CRIAR PEDIDO
# ==========================================================

@router.post("/")
def criar_pedido(
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):

    # ------------------------------------------------------
    # BUSCAR CARRINHO DO USUÁRIO
    # ------------------------------------------------------

    carrinho = db.query(CarrinhoDB).filter(
        CarrinhoDB.usuario_id == usuario.id
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=404,
            detail="Carrinho não encontrado"
        )

    # ------------------------------------------------------
    # BUSCAR ITENS DO CARRINHO
    # ------------------------------------------------------

    itens_carrinho = db.query(CarrinhoItemDB).filter(
        CarrinhoItemDB.carrinho_id == carrinho.id
    ).all()

    if not itens_carrinho:
        raise HTTPException(
            status_code=400,
            detail="Carrinho vazio"
        )

    # ------------------------------------------------------
    # VERIFICAR ESTOQUE E CALCULAR TOTAL
    # ------------------------------------------------------

    total = 0

    for item in itens_carrinho:

        produto = db.query(ProdutoDB).filter(
            ProdutoDB.id == item.produto_id
        ).first()

        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.produto_id} não encontrado"
            )

        if not produto.ativo:
            raise HTTPException(
                status_code=400,
                detail=f"Produto '{produto.nome}' está inativo"
            )

        if produto.estoque < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para o produto '{produto.nome}'"
            )

        total += produto.preco * item.quantidade

    # ------------------------------------------------------
    # BUSCAR ENDEREÇO DO USUÁRIO
    # ------------------------------------------------------

    endereco = db.query(EnderecoDB).filter(
        EnderecoDB.usuario_id == usuario.id
    ).first()

    if not endereco:
        raise HTTPException(
            status_code=400,
            detail="Usuário não possui endereço cadastrado"
        )

    # ------------------------------------------------------
    # CRIAR PEDIDO
    # ------------------------------------------------------

    novo_pedido = PedidoDB(
        usuario_id=usuario.id,
        endereco_id=endereco.id,
        total=total,
        status="PENDENTE"
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    # ------------------------------------------------------
    # CRIAR ITENS DO PEDIDO
    # ------------------------------------------------------

    for item in itens_carrinho:

        produto = db.query(ProdutoDB).filter(
            ProdutoDB.id == item.produto_id
        ).first()

        novo_item = PedidoItemDB(
            pedido_id=novo_pedido.id,
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco
        )

        db.add(novo_item)

        # Diminuir estoque
        produto.estoque -= item.quantidade

    # ------------------------------------------------------
    # LIMPAR CARRINHO
    # ------------------------------------------------------

    for item in itens_carrinho:
        db.delete(item)

    db.commit()

    # ------------------------------------------------------
    # RETORNAR PEDIDO
    # ------------------------------------------------------

    return {
        "mensagem": "Pedido criado com sucesso",
        "pedido_id": novo_pedido.id,
        "usuario_id": novo_pedido.usuario_id,
        "total": novo_pedido.total,
        "status": novo_pedido.status
    }


# ==========================================================
# LISTAR PEDIDOS DO USUÁRIO
# ==========================================================

@router.get("/")
def listar_pedidos(
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):

    pedidos = db.query(PedidoDB).filter(
        PedidoDB.usuario_id == usuario.id
    ).all()

    return pedidos


# ==========================================================
# BUSCAR PEDIDO POR ID
# ==========================================================

@router.get("/{pedido_id}")
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):

    pedido = db.query(PedidoDB).filter(
        PedidoDB.id == pedido_id,
        PedidoDB.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return pedido


# ==========================================================
# ATUALIZAR STATUS DO PEDIDO
# ==========================================================

@router.put("/{pedido_id}/status")
def atualizar_status_pedido(
    pedido_id: int,
    status: str,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):

    pedido = db.query(PedidoDB).filter(
        PedidoDB.id == pedido_id,
        PedidoDB.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    status_permitidos = [
        "PENDENTE",
        "PAGO",
        "ENVIADO",
        "ENTREGUE",
        "CANCELADO"
    ]

    if status not in status_permitidos:
        raise HTTPException(
            status_code=400,
            detail="Status inválido"
        )

    pedido.status = status

    db.commit()
    db.refresh(pedido)

    return {
        "mensagem": "Status atualizado com sucesso",
        "pedido_id": pedido.id,
        "status": pedido.status
    }

