from pydantic import BaseModel
from typing import Optional

class PagamentoBase(BaseModel):
    valor: float
    forma: str
    tipo_pagamento: str

class PagamentoCreate(PagamentoBase):
    id_usuario_cadastrou: int

class PagamentoResponse(BaseModel):
    id_pagamento: int
    valor: float
    forma: str
    tipo_pagamento: str
    id_usuario_cadastrou: Optional[int] = None
    
    class Config:
        from_attributes = True

class PagComandaCreate(BaseModel):
    id_pagamento: int
    id_comanda: int

class PagReservaCreate(BaseModel):
    id_pagamento: int
    id_reserva: int
    cpf_cliente: str
    porcentagem: float

class PagCompraCreate(BaseModel):
    id_pagamento: int
    id_compra: int
