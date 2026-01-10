from pydantic import BaseModel
from typing import Optional
from datetime import date

class CompraBase(BaseModel):
    data: date
    valor_total: float
    cpf_cliente: str

class CompraCreate(CompraBase):
    id_usuario_cadastrou: int

class CompraResponse(BaseModel):
    id_compra: int
    data: date
    valor_total: float
    cpf_cliente: str
    id_usuario_cadastrou: Optional[int] = None
    
    class Config:
        from_attributes = True

class ItemCompraBase(BaseModel):
    id_compra: int
    id_produto: int
    quantidade: int
    preco_unitario: float

class ItemCompraCreate(ItemCompraBase):
    pass

class ItemCompraResponse(ItemCompraBase):
    class Config:
        from_attributes = True
