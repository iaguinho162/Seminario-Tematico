from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="Marketplace API")

# Simulações em memória
users_db = {}
products_db = {}
orders_db = {}

# Models
class User(BaseModel):
    id: str = None
    name: str
    email: str

class Product(BaseModel):
    id: str = None
    name: str
    description: str
    price: float
    stock: int

class Order(BaseModel):
    id: str = None
    user_id: str
    product_ids: List[str]

# Rotas de Usuários
@app.post("/users/", response_model=User)
def create_user(user: User):
    user.id = str(uuid4())
    users_db[user.id] = user
    return user

@app.get("/users/", response_model=List[User])
def list_users():
    return list(users_db.values())

# Rotas de Produtos
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    product.id = str(uuid4())
    products_db[product.id] = product
    return product

@app.get("/products/", response_model=List[Product])
def list_products():
    return list(products_db.values())

# Rotas de Pedidos
@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    if order.user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    for pid in order.product_ids:
        if pid not in products_db:
            raise HTTPException(status_code=404, detail=f"Produto {pid} não encontrado")
        if products_db[pid].stock < 1:
            raise HTTPException(status_code=400, detail=f"Produto {pid} sem estoque")
    
    # Deduz do estoque
    for pid in order.product_ids:
        products_db[pid].stock -= 1

    order.id = str(uuid4())
    orders_db[order.id] = order
    return order

@app.get("/orders/", response_model=List[Order])
def list_orders():
    return list(orders_db.values())