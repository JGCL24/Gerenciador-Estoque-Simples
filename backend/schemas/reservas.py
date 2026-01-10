from pydantic import BaseModel
from typing import Optional
from datetime import date

class ReservaBase(BaseModel):
    data: date
    quant_horas: int
    status: str
    cpf_cliente: str
    id_campo: int

class ReservaCreate(ReservaBase):
    id_usuario_cadastrou: int

class ReservaResponse(BaseModel):
    id_reserva: int
    data: date
    quant_horas: int
    status: str
    cpf_cliente: str
    id_campo: int
    id_usuario_cadastrou: Optional[int] = None
    
    class Config:
        from_attributes = True
