from pydantic import BaseModel

class CampoBase(BaseModel):
    numero: int
    status: str

class CampoCreate(CampoBase):
    pass

class CampoResponse(BaseModel):
    id_campo: int
    numero: int
    status: str
    
    class Config:
        from_attributes = True
