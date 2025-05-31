from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
