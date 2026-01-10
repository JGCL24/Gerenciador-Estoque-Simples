from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str
    senha: str
    tipo_usuario: str

class UsuarioCreate(UsuarioBase):
    id_usuario: int

class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    tipo_usuario: str
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    id_usuario: int
    senha: str
