from pydantic import BaseModel


class EnderecoCreate(BaseModel):
    cep: str
    rua: str
    numero: str
    complemento: str | None = None
    bairro: str
    cidade: str
    estado: str


class EnderecoResponse(BaseModel):
    id: int
    cep: str
    rua: str
    numero: str
    complemento: str | None
    bairro: str
    cidade: str
    estado: str

    class Config:
        from_attributes = True