from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import UsuarioCreate, UsuarioResponse, UsuarioLogin
import hashlib

router = APIRouter()

@router.post("/", response_model=UsuarioResponse, status_code=201)
async def criar_usuario(usuario: UsuarioCreate):
    """Cria um novo usuário"""
    try:
        # Verifica se já existe usuário com mesmo ID
        query_check = "SELECT * FROM Usuario WHERE Id_Usuario = %s"
        existing = db.execute_query(query_check, (usuario.id_usuario,))
        if existing:
            raise HTTPException(status_code=400, detail="Usuário com este ID já existe")
        
        # Hash da senha (simples, em produção usar bcrypt)
        senha_hash = hashlib.sha256(usuario.senha.encode()).hexdigest()
        
        query = """
            INSERT INTO Usuario (Id_Usuario, Nome, Senha, Tipo_Usuario)
            VALUES (%s, %s, %s, %s)
            RETURNING Id_Usuario, Nome, Tipo_Usuario
        """
        result = db.execute_query(query, (
            usuario.id_usuario, usuario.nome, senha_hash, usuario.tipo_usuario
        ))
        
        if result:
            return UsuarioResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios():
    """Lista todos os usuários"""
    try:
        query = "SELECT Id_Usuario, Nome, Tipo_Usuario FROM Usuario"
        result = db.execute_query(query)
        return [UsuarioResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")

@router.get("/{id_usuario}", response_model=UsuarioResponse)
async def obter_usuario(id_usuario: int):
    """Obtém um usuário por ID"""
    try:
        query = "SELECT Id_Usuario, Nome, Tipo_Usuario FROM Usuario WHERE Id_Usuario = %s"
        result = db.execute_query(query, (id_usuario,))
        if not result:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return UsuarioResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter usuário: {str(e)}")

@router.put("/{id_usuario}", response_model=UsuarioResponse)
async def atualizar_usuario(id_usuario: int, usuario: UsuarioCreate):
    """Atualiza um usuário"""
    try:
        # Verifica se existe
        query_check = "SELECT * FROM Usuario WHERE Id_Usuario = %s"
        existing = db.execute_query(query_check, (id_usuario,))
        if not existing:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        senha_hash = hashlib.sha256(usuario.senha.encode()).hexdigest()
        
        query = """
            UPDATE Usuario 
            SET Nome = %s, Senha = %s, Tipo_Usuario = %s
            WHERE Id_Usuario = %s
            RETURNING Id_Usuario, Nome, Tipo_Usuario
        """
        result = db.execute_query(query, (
            usuario.nome, senha_hash, usuario.tipo_usuario, id_usuario
        ))
        
        if result:
            return UsuarioResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar usuário: {str(e)}")

@router.delete("/{id_usuario}", status_code=204)
async def deletar_usuario(id_usuario: int):
    """Deleta um usuário"""
    try:
        query_check = "SELECT * FROM Usuario WHERE Id_Usuario = %s"
        existing = db.execute_query(query_check, (id_usuario,))
        if not existing:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        query = "DELETE FROM Usuario WHERE Id_Usuario = %s"
        db.execute_query(query, (id_usuario,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar usuário: {str(e)}")

@router.post("/login")
async def login(credentials: UsuarioLogin):
    """Autentica um usuário"""
    try:
        senha_hash = hashlib.sha256(credentials.senha.encode()).hexdigest()
        query = """
            SELECT Id_Usuario, Nome, Tipo_Usuario 
            FROM Usuario 
            WHERE Id_Usuario = %s AND Senha = %s
        """
        result = db.execute_query(query, (credentials.id_usuario, senha_hash))
        if not result:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        return {"message": "Login bem-sucedido", "usuario": UsuarioResponse(**result[0])}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer login: {str(e)}")
