from fastapi import APIRouter, HTTPException
from models import Pedido
from uuid import uuid4
import requests

router = APIRouter()

# Banco de dados em memória para pedidos
banco_pedidos = {}

# URLs dos outros serviços
URL_USUARIOS = "http://users:8000"
URL_PRODUTOS = "http://products:8000"

# Criar um pedido
@router.post("/pedidos/", response_model=Pedido)
def criar_pedido(pedido: Pedido):
    # Verificar se o usuário existe
    resposta_usuario = requests.get(f"{URL_USUARIOS}/usuarios/{pedido.usuario_id}")
    if resposta_usuario.status_code != 200:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Verificar se os produtos existem
    for pid in pedido.produtos_ids:
        resposta_produto = requests.get(f"{URL_PRODUTOS}/produtos/{pid}")
        if resposta_produto.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Produto {pid} não encontrado")
    
    pedido.id = str(uuid4())
    banco_pedidos[pedido.id] = pedido

    return pedido

# Listar todos os pedidos
@router.get("/pedidos/")
def listar_pedidos():
    return list(banco_pedidos.values())
