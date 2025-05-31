from fastapi import APIRouter, HTTPException
from models import Produto
from uuid import uuid4

router = APIRouter()

# Banco de dados em memória simulando os produtos
banco_produtos = {}

# Criar um produto
@router.post("/produtos/", response_model=Produto)
def criar_produto(produto: Produto):
    produto.id = str(uuid4())
    banco_produtos[produto.id] = produto
    return produto

# Listar todos os produtos
@router.get("/produtos/")
def listar_produtos():
    return list(banco_produtos.values())

# Buscar um produto específico por ID
@router.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: str):
    produto = banco_produtos.get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto
