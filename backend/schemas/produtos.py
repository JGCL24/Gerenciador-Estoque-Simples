from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    validade: Optional[date] = None
    quant_min_estoque: int

class ProdutoCreate(ProdutoBase):
    id_admin_cadastrou: int

class ProdutoResponse(BaseModel):
    id_produto: int
    nome: str
    preco: float
    validade: Optional[date] = None
    quant_min_estoque: int
    id_admin_cadastrou: Optional[int] = None
    
    class Config:
        from_attributes = True
