from fastapi import FastAPI

from app.database import engine, Base

from app import models

from app.routes import produtos
from app.routes import categorias
from app.routes import usuarios
from app.routes import carrinho
from app.routes import pedidos
from app.routes import auth


app = FastAPI(

    title="E-commerce API",

    description="API de um sistema de e-commerce",

    version="1.0.0"

)


Base.metadata.create_all(bind=engine)


app.include_router(produtos.router)
app.include_router(categorias.router)
app.include_router(usuarios.router)
app.include_router(carrinho.router)
app.include_router(pedidos.router)
app.include_router(auth.router)


@app.get("/")
def inicio():

    return {
        "mensagem": "E-commerce API funcionando!"
    }