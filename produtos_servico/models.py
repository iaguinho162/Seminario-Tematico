from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

class Produto(BaseModel):
    id: Optional[str] = None
    nome: str
    descricao: str
    preco: float
    