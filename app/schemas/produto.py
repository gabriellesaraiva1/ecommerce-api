from pydantic import BaseModel, Field


class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    descricao: str | None = Field(default=None, max_length=500)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)
    categoria_id: int | None = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: float
    estoque: int
    ativo: bool
    categoria_id: int | None

    class Config:
        from_attributes = True


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=100)
    descricao: str | None = Field(default=None, max_length=500)
    preco: float | None = Field(default=None, gt=0)
    estoque: int | None = Field(default=None, ge=0)
    ativo: bool | None = None
    categoria_id: int | None = None