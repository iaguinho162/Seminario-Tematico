from pydantic import BaseModel
from typing import Optional, List

class Pedido(BaseModel):
    id: Optional[str] = None
    usuario_id: str
    produtos_ids: List[str]
