from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nome: str = Field(
        min_length=3,
        max_length=100
    )

    descricao: str | None = Field(
        default=None,
        max_length=300
    )


class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    ativo: bool

    class Config:
        from_attributes = True


class CategoriaUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    descricao: str | None = Field(
        default=None,
        max_length=300
    )

    ativo: bool | None = None