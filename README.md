# 🛒 E-commerce API

API REST desenvolvida com **FastAPI** para gerenciamento de um sistema de e-commerce, incluindo produtos, categorias, usuários, autenticação e pedidos.

O projeto foi desenvolvido com foco em boas práticas de desenvolvimento backend, organização de código e construção de APIs REST.

## 🚀 Tecnologias

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* Bcrypt
* Uvicorn
* Swagger / OpenAPI

## 📌 Funcionalidades

### 👤 Usuários

* Cadastro de usuários
* Consulta de usuários
* Atualização de usuários
* Autenticação
* Criptografia de senha
* Autenticação utilizando JWT
* Proteção de endpoints

### 📦 Produtos

* Cadastro de produtos
* Listagem de produtos
* Consulta de produto por ID
* Atualização de produtos
* Exclusão de produtos
* Controle de estoque
* Associação com categorias

### 🗂️ Categorias

* Cadastro de categorias
* Listagem de categorias
* Consulta por ID
* Atualização de categorias
* Exclusão de categorias
* Ativação e desativação

### 🛒 Carrinho

* Criação de carrinho
* Adição de produtos
* Controle de quantidade
* Consulta do carrinho
* Remoção de itens

### 📋 Pedidos

* Criação de pedidos
* Consulta de pedidos
* Controle dos itens do pedido
* Integração com usuário autenticado

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Token)** para autenticação.

Após realizar o login, o usuário recebe um token que deve ser enviado no cabeçalho das requisições protegidas:

```text
Authorization: Bearer SEU_TOKEN
```

## 📂 Estrutura do projeto

```text
ecommerce-api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── dependencies.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   └── routes/
│       ├── produtos.py
│       ├── categorias.py
│       ├── usuarios.py
│       ├── auth.py
│       ├── carrinho.py
│       └── pedidos.py
│
├── .venv/
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/gabriellesaraiva1/ecommerce-api.git
```

### 2. Entrar na pasta

```bash
cd ecommerce-api
```

### 3. Criar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

### 4. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 6. Executar a API

```powershell
uvicorn app.main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

## 📚 Documentação da API

O projeto utiliza Swagger/OpenAPI.

Após iniciar a aplicação, acesse:

```text
http://127.0.0.1:8000/docs
```

Também é possível acessar a documentação alternativa:

```text
http://127.0.0.1:8000/redoc
```

## 🧪 Testes

Os endpoints podem ser testados diretamente pelo **Swagger**, utilizando:

```text
http://127.0.0.1:8000/docs
```

É possível testar:

* Cadastro e login
* Autenticação JWT
* Produtos
* Categorias
* Usuários
* Carrinho
* Pedidos

## 🎯 Objetivo do projeto

Este projeto faz parte dos meus estudos em **desenvolvimento backend com Python e FastAPI**, com o objetivo de desenvolver conhecimentos em:

* Desenvolvimento de APIs REST
* Arquitetura backend
* Bancos de dados relacionais
* SQLAlchemy
* Autenticação e autorização
* JWT
* Validação de dados
* CRUD
* Relacionamentos entre entidades
* Documentação de APIs

## 👨‍💻 Autor

**Gabrielle Saraiva**

Estudante de Análise e Desenvolvimento de Sistemas, com foco em desenvolvimento backend, dados e tecnologias Python.

---


