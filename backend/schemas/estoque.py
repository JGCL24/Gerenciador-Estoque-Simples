from pydantic import BaseModel
from datetime import date

class EstoqueBase(BaseModel):
    id_produto: int
    quant_present: int

class EstoqueCreate(EstoqueBase):
    pass

class EstoqueResponse(BaseModel):
    id_estoque: int
    id_produto: int
    quant_present: int
    
    class Config:
        from_attributes = True

class MovimentaBase(BaseModel):
    id_estoque: int
    tipo: str
    quantidade: int
    data: date

class MovimentaCreate(MovimentaBase):
    pass

class MovimentaResponse(BaseModel):
    id_movimenta: int
    id_estoque: int
    tipo: str
    quantidade: int
    data: date
    
    class Config:
        from_attributes = True
