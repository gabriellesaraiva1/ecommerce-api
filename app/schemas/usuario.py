from pydantic import BaseModel, Field


class UsuarioCreate(BaseModel):
    nome: str = Field(
        min_length=3,
        max_length=100
    )

    email: str = Field(
        min_length=5,
        max_length=150
    )

    senha: str = Field(
        min_length=6,
        max_length=100
    )


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: str | None = Field(
        default=None,
        min_length=5,
        max_length=150
    )

    senha: str | None = Field(
        default=None,
        min_length=6,
        max_length=100
    )

    ativo: bool | None = None