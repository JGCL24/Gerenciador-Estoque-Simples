from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import ClienteCreate, ClienteResponse

router = APIRouter()

@router.post("/", response_model=ClienteResponse, status_code=201)
async def criar_cliente(cliente: ClienteCreate):
    """Cria um novo cliente"""
    try:
        # Verifica se já existe cliente com mesmo CPF
        query_check = "SELECT * FROM Cliente WHERE CPF = %s"
        existing = db.execute_query(query_check, (cliente.cpf,))
        if existing:
            raise HTTPException(status_code=400, detail="Cliente com este CPF já existe")
        
        query = """
            INSERT INTO Cliente (CPF, Nome, Email, Tipo, Id_Usuario_Cadastrou)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING CPF, Nome, Email, Tipo, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            cliente.cpf, cliente.nome, cliente.email, cliente.tipo, cliente.id_usuario_cadastrou
        ))
        
        if result:
            return ClienteResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar cliente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {str(e)}")

@router.get("/", response_model=List[ClienteResponse])
async def listar_clientes():
    """Lista todos os clientes"""
    try:
        query = "SELECT CPF, Nome, Email, Tipo, Id_Usuario_Cadastrou FROM Cliente"
        result = db.execute_query(query)
        return [ClienteResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@router.get("/{cpf}", response_model=ClienteResponse)
async def obter_cliente(cpf: str):
    """Obtém um cliente por CPF"""
    try:
        query = "SELECT CPF, Nome, Email, Tipo, Id_Usuario_Cadastrou FROM Cliente WHERE CPF = %s"
        result = db.execute_query(query, (cpf,))
        if not result:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return ClienteResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter cliente: {str(e)}")

@router.put("/{cpf}", response_model=ClienteResponse)
async def atualizar_cliente(cpf: str, cliente: ClienteCreate):
    """Atualiza um cliente"""
    try:
        query_check = "SELECT * FROM Cliente WHERE CPF = %s"
        existing = db.execute_query(query_check, (cpf,))
        if not existing:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        query = """
            UPDATE Cliente 
            SET Nome = %s, Email = %s, Tipo = %s, Id_Usuario_Cadastrou = %s
            WHERE CPF = %s
            RETURNING CPF, Nome, Email, Tipo, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            cliente.nome, cliente.email, cliente.tipo, cliente.id_usuario_cadastrou, cpf
        ))
        
        if result:
            return ClienteResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar cliente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")

@router.delete("/{cpf}", status_code=204)
async def deletar_cliente(cpf: str):
    """Deleta um cliente"""
    try:
        query_check = "SELECT * FROM Cliente WHERE CPF = %s"
        existing = db.execute_query(query_check, (cpf,))
        if not existing:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        query = "DELETE FROM Cliente WHERE CPF = %s"
        db.execute_query(query, (cpf,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente: {str(e)}")
