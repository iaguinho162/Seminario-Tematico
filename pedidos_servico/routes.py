from fastapi import APIRouter, HTTPException, Query
from models import Pedido
from uuid import uuid4
import requests
import mercadopago
from fastapi.responses import JSONResponse



router = APIRouter()

# Banco de dados em memória para pedidos
banco_pedidos = {}

# URLs dos outros serviços
URL_USUARIOS = "http://users:8000"
URL_PRODUTOS = "http://products:8000"

# Token do Mercado Pago
ACCESS_TOKEN = "TEST-3547866413447504-053117-35568f2c0ec65d083045cde33e6484f4-572486490"
sdk = mercadopago.SDK(ACCESS_TOKEN)


#Criar um pedido
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


#Listar formas de pagamento disponíveis no Mercado Pago
@router.get("/formas-pagamento/", response_model=dict)
def listar_formas_pagamento():
    url = "https://api.mercadopago.com/v1/payment_methods"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Formas de pagamento não encontradas")

    dados = response.json()

    formas = [
        {
            "id": item["id"],
            "nome": item["name"],
            "tipo_pagamento": item["payment_type_id"],
            "status": item["status"]
        }
        for item in dados
    ]

    return {"formas_pagamento": formas}


#Criar pagamento de um pedido
@router.post("/pagamento/{pedido_id}")
def criar_pagamento(
    pedido_id: str,
    metodo_pagamento: str = Query(..., description="pix, bolbradesco, visa, master, etc.")
):
    # Verificar se o pedido existe
    pedido = banco_pedidos.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Obter informações do usuário
    resposta_usuario = requests.get(f"{URL_USUARIOS}/usuarios/{pedido.usuario_id}")
    if resposta_usuario.status_code != 200:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario = resposta_usuario.json()

    # Calcular o valor total do pedido (somar todos os produtos)
    total = 0
    for pid in pedido.produtos_ids:
        resposta_produto = requests.get(f"{URL_PRODUTOS}/produtos/{pid}")
        if resposta_produto.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Produto {pid} não encontrado")
        produto = resposta_produto.json()
        total += float(produto["preco"])

    # Montar os dados do pagamento
    payment_data = {
        "transaction_amount": total,
        "description": f"Pagamento do pedido {pedido_id}",
        "payment_method_id": metodo_pagamento,
        "payer": {
            "email": usuario["email"],
            "first_name": usuario["nome"],
            "last_name": "Cliente",  # Opcional, pode ser fixo ou adicionado depois no modelo
            "identification": {
                "type": "CPF",
                "number": usuario["cpf"]
            }
        }
    }

    # Enviar requisição para Mercado Pago
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    if "id" not in payment:
        raise HTTPException(status_code=400, detail="Erro ao criar pagamento.")

    return JSONResponse(content={
        "id_pagamento": payment["id"],
        "status": payment["status"],
        "status_detail": payment["status_detail"],
        "qr_code": payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code"),
        "qr_code_base64": payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64"),
        "link_mercado_pago": payment.get("point_of_interaction", {}).get("transaction_data", {}).get("ticket_url")
    })


