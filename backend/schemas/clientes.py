from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    cpf: str
    nome: str
    email: str
    tipo: str

class ClienteCreate(ClienteBase):
    id_usuario_cadastrou: int

class ClienteResponse(ClienteBase):
    id_usuario_cadastrou: Optional[int] = None
    
    class Config:
        from_attributes = True
