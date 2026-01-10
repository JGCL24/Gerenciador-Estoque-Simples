from pydantic import BaseModel
from datetime import date

class ComandaBase(BaseModel):
    data: date
    status: str
    numero_mesa: int
    cpf_cliente: str
    id_funcionario: int

class ComandaCreate(ComandaBase):
    pass

class ComandaResponse(BaseModel):
    id_comanda: int
    data: date
    status: str
    numero_mesa: int
    cpf_cliente: str
    id_funcionario: int
    
    class Config:
        from_attributes = True

class ItemComandaBase(BaseModel):
    id_comanda: int
    id_produto: int
    quantidade: int
    preco_unitario: float

class ItemComandaCreate(ItemComandaBase):
    pass

class ItemComandaResponse(ItemComandaBase):
    class Config:
        from_attributes = True
