from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import MesaCreate, MesaResponse

router = APIRouter()

@router.post("/", response_model=MesaResponse, status_code=201)
async def criar_mesa(mesa: MesaCreate):
    """Cria uma nova mesa"""
    try:
        # Verifica se já existe mesa com mesmo número
        query_check = "SELECT * FROM Mesa WHERE Numero = %s"
        existing = db.execute_query(query_check, (mesa.numero,))
        if existing:
            raise HTTPException(status_code=400, detail="Mesa com este número já existe")
        
        query = """
            INSERT INTO Mesa (Numero, Status)
            VALUES (%s, %s)
            RETURNING Numero, Status
        """
        result = db.execute_query(query, (mesa.numero, mesa.status))
        
        if result:
            return MesaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar mesa")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar mesa: {str(e)}")

@router.get("/", response_model=List[MesaResponse])
async def listar_mesas():
    """Lista todas as mesas"""
    try:
        query = "SELECT Numero, Status FROM Mesa ORDER BY Numero"
        result = db.execute_query(query)
        return [MesaResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar mesas: {str(e)}")

@router.get("/{numero}", response_model=MesaResponse)
async def obter_mesa(numero: int):
    """Obtém uma mesa por número"""
    try:
        query = "SELECT Numero, Status FROM Mesa WHERE Numero = %s"
        result = db.execute_query(query, (numero,))
        if not result:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
        return MesaResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter mesa: {str(e)}")

@router.put("/{numero}", response_model=MesaResponse)
async def atualizar_mesa(numero: int, mesa: MesaCreate):
    """Atualiza uma mesa"""
    try:
        query_check = "SELECT * FROM Mesa WHERE Numero = %s"
        existing = db.execute_query(query_check, (numero,))
        if not existing:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
        
        query = """
            UPDATE Mesa 
            SET Status = %s
            WHERE Numero = %s
            RETURNING Numero, Status
        """
        result = db.execute_query(query, (mesa.status, numero))
        
        if result:
            return MesaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar mesa")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar mesa: {str(e)}")

@router.delete("/{numero}", status_code=204)
async def deletar_mesa(numero: int):
    """Deleta uma mesa"""
    try:
        query_check = "SELECT * FROM Mesa WHERE Numero = %s"
        existing = db.execute_query(query_check, (numero,))
        if not existing:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
        
        query = "DELETE FROM Mesa WHERE Numero = %s"
        db.execute_query(query, (numero,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar mesa: {str(e)}")
