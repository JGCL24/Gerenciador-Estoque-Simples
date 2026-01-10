from pydantic import BaseModel

class MesaBase(BaseModel):
    numero: int
    status: str

class MesaCreate(MesaBase):
    pass

class MesaResponse(MesaBase):
    class Config:
        from_attributes = True
