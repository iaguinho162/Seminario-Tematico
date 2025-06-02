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

@router.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: str, dados_produto: Produto):
    if produto_id not in banco_produtos:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    dados_produto.id = produto_id
    banco_produtos[produto_id] = dados_produto
    return dados_produto


@router.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: str):
    if produto_id not in banco_produtos:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    del banco_produtos[produto_id]
    return {"detail": "Produto deletado com sucesso"}