from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import CampoCreate, CampoResponse

router = APIRouter()

@router.post("/", response_model=CampoResponse, status_code=201)
async def criar_campo(campo: CampoCreate):
    """Cria um novo campo"""
    try:
        query = """
            INSERT INTO Campo (Numero, Status)
            VALUES (%s, %s)
            RETURNING Id_Campo, Numero, Status
        """
        result = db.execute_query(query, (campo.numero, campo.status))
        
        if result:
            return CampoResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar campo")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar campo: {str(e)}")

@router.get("/", response_model=List[CampoResponse])
async def listar_campos():
    """Lista todos os campos"""
    try:
        query = "SELECT Id_Campo, Numero, Status FROM Campo"
        result = db.execute_query(query)
        return [CampoResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar campos: {str(e)}")

@router.get("/{id_campo}", response_model=CampoResponse)
async def obter_campo(id_campo: int):
    """Obtém um campo por ID"""
    try:
        query = "SELECT Id_Campo, Numero, Status FROM Campo WHERE Id_Campo = %s"
        result = db.execute_query(query, (id_campo,))
        if not result:
            raise HTTPException(status_code=404, detail="Campo não encontrado")
        return CampoResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter campo: {str(e)}")

@router.put("/{id_campo}", response_model=CampoResponse)
async def atualizar_campo(id_campo: int, campo: CampoCreate):
    """Atualiza um campo"""
    try:
        query_check = "SELECT * FROM Campo WHERE Id_Campo = %s"
        existing = db.execute_query(query_check, (id_campo,))
        if not existing:
            raise HTTPException(status_code=404, detail="Campo não encontrado")
        
        query = """
            UPDATE Campo 
            SET Numero = %s, Status = %s
            WHERE Id_Campo = %s
            RETURNING Id_Campo, Numero, Status
        """
        result = db.execute_query(query, (campo.numero, campo.status, id_campo))
        
        if result:
            return CampoResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar campo")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar campo: {str(e)}")

@router.delete("/{id_campo}", status_code=204)
async def deletar_campo(id_campo: int):
    """Deleta um campo"""
    try:
        query_check = "SELECT * FROM Campo WHERE Id_Campo = %s"
        existing = db.execute_query(query_check, (id_campo,))
        if not existing:
            raise HTTPException(status_code=404, detail="Campo não encontrado")
        
        query = "DELETE FROM Campo WHERE Id_Campo = %s"
        db.execute_query(query, (id_campo,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar campo: {str(e)}")
