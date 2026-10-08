from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# ==========================================================
# CATEGORIA
# ==========================================================

class CategoriaDB(Base):
    __tablename__ = "categorias"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False,
        unique=True
    )

    descricao = Column(
        String(300),
        nullable=True
    )

    ativo = Column(
        Boolean,
        default=True
    )

    produtos = relationship(
        "ProdutoDB",
        back_populates="categoria"
    )


# ==========================================================
# PRODUTO
# ==========================================================

class ProdutoDB(Base):
    __tablename__ = "produtos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    descricao = Column(
        String(500),
        nullable=True
    )

    preco = Column(
        Float,
        nullable=False
    )

    estoque = Column(
        Integer,
        nullable=False,
        default=0
    )

    ativo = Column(
        Boolean,
        default=True
    )

    data_criacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    categoria_id = Column(
        Integer,
        ForeignKey("categorias.id"),
        nullable=True
    )

    categoria = relationship(
        "CategoriaDB",
        back_populates="produtos"
    )


# ==========================================================
# USUÁRIO
# ==========================================================

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True
    )

    senha = Column(
        String(255),
        nullable=False
    )

    ativo = Column(
        Boolean,
        default=True
    )

    data_criacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Um usuário possui um carrinho
    carrinho = relationship(
        "CarrinhoDB",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )


# ==========================================================
# CARRINHO
# ==========================================================

class CarrinhoDB(Base):
    __tablename__ = "carrinhos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        unique=True
    )

    data_criacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relacionamento com usuário
    usuario = relationship(
        "UsuarioDB",
        back_populates="carrinho"
    )

    # Um carrinho possui vários itens
    itens = relationship(
        "CarrinhoItemDB",
        back_populates="carrinho",
        cascade="all, delete-orphan"
    )


# ==========================================================
# ITEM DO CARRINHO
# ==========================================================

class CarrinhoItemDB(Base):
    __tablename__ = "carrinho_itens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    carrinho_id = Column(
        Integer,
        ForeignKey("carrinhos.id"),
        nullable=False
    )

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = Column(
        Integer,
        nullable=False,
        default=1
    )

    # Relacionamento com carrinho
    carrinho = relationship(
        "CarrinhoDB",
        back_populates="itens"
    )

    # Relacionamento com produto
    produto = relationship(
        "ProdutoDB"
    )


# ==========================================================
# ENDEREÇO
# ==========================================================

class EnderecoDB(Base):
    __tablename__ = "enderecos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    cep = Column(
        String(10),
        nullable=False
    )

    rua = Column(
        String(150),
        nullable=False
    )

    numero = Column(
        String(20),
        nullable=False
    )

    complemento = Column(
        String(100),
        nullable=True
    )

    bairro = Column(
        String(100),
        nullable=False
    )

    cidade = Column(
        String(100),
        nullable=False
    )

    estado = Column(
        String(2),
        nullable=False
    )

    # Relacionamento com usuário
    usuario = relationship(
        "UsuarioDB"
    )

    # Um endereço pode estar associado a vários pedidos
    pedidos = relationship(
        "PedidoDB",
        back_populates="endereco"
    )


# ==========================================================
# PEDIDO
# ==========================================================

class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    endereco_id = Column(
        Integer,
        ForeignKey("enderecos.id"),
        nullable=False
    )

    total = Column(
        Float,
        nullable=False,
        default=0
    )

    status = Column(
        String(30),
        nullable=False,
        default="PENDENTE"
    )

    data_criacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relacionamento com usuário
    usuario = relationship(
        "UsuarioDB"
    )

    # Relacionamento com endereço
    endereco = relationship(
        "EnderecoDB",
        back_populates="pedidos"
    )

    # Um pedido possui vários itens
    itens = relationship(
        "PedidoItemDB",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )


# ==========================================================
# ITEM DO PEDIDO
# ==========================================================

class PedidoItemDB(Base):
    __tablename__ = "pedido_itens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pedido_id = Column(
        Integer,
        ForeignKey("pedidos.id"),
        nullable=False
    )

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = Column(
        Integer,
        nullable=False
    )

    # Guarda o preço no momento da compra
    preco_unitario = Column(
        Float,
        nullable=False
    )

    # Relacionamento com pedido
    pedido = relationship(
        "PedidoDB",
        back_populates="itens"
    )

    # Relacionamento com produto
    produto = relationship(
        "ProdutoDB"
    )