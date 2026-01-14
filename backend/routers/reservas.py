from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import ReservaCreate, ReservaResponse

router = APIRouter()

@router.post("/", response_model=ReservaResponse, status_code=201)
async def criar_reserva(reserva: ReservaCreate):
    """Cria uma nova reserva"""
    try:
        # Verifica se o campo existe
        query_campo = "SELECT * FROM Campo WHERE Id_Campo = %s"
        campo = db.execute_query(query_campo, (reserva.id_campo,))
        if not campo:
            raise HTTPException(status_code=404, detail="Campo não encontrado")
        # Verifica se o cliente existe
        query_cliente = "SELECT * FROM Cliente WHERE CPF = %s"
        cliente = db.execute_query(query_cliente, (reserva.cpf_cliente,))
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        query = """
            INSERT INTO Reserva (Data, Quant_Horas, Status, CPF_Cliente, Id_Campo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING Id_Reserva, Data, Quant_Horas, Status, CPF_Cliente, Id_Campo, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            reserva.data, reserva.quant_horas, reserva.status,
            reserva.cpf_cliente, reserva.id_campo
        ))
        if result:
            return ReservaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar reserva")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar reserva: {str(e)}")

@router.get("/", response_model=List[ReservaResponse])
async def listar_reservas():
    """Lista todas as reservas"""
    try:
        query = """
            SELECT Id_Reserva, Data, Quant_Horas, Status, CPF_Cliente, Id_Campo, Id_Usuario_Cadastrou
            FROM Reserva
            ORDER BY Data DESC
        """
        result = db.execute_query(query)
        return [ReservaResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar reservas: {str(e)}")

@router.get("/{id_reserva}", response_model=ReservaResponse)
async def obter_reserva(id_reserva: int):
    """Obtém uma reserva por ID"""
    try:
        query = """
            SELECT Id_Reserva, Data, Quant_Horas, Status, CPF_Cliente, Id_Campo, Id_Usuario_Cadastrou
            FROM Reserva WHERE Id_Reserva = %s
        """
        result = db.execute_query(query, (id_reserva,))
        if not result:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        return ReservaResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter reserva: {str(e)}")

@router.get("/cliente/{cpf}", response_model=List[ReservaResponse])
async def listar_reservas_cliente(cpf: str):
    """Lista todas as reservas de um cliente"""
    try:
        query = """
            SELECT Id_Reserva, Data, Quant_Horas, Status, CPF_Cliente, Id_Campo, Id_Usuario_Cadastrou
            FROM Reserva WHERE CPF_Cliente = %s
            ORDER BY Data DESC
        """
        result = db.execute_query(query, (cpf,))
        return [ReservaResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar reservas do cliente: {str(e)}")

@router.put("/{id_reserva}", response_model=ReservaResponse)
async def atualizar_reserva(id_reserva: int, reserva: ReservaCreate):
    """Atualiza uma reserva"""
    try:
        query_check = "SELECT * FROM Reserva WHERE Id_Reserva = %s"
        existing = db.execute_query(query_check, (id_reserva,))
        if not existing:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        
        query = """
            UPDATE Reserva 
            SET Data = %s, Quant_Horas = %s, Status = %s, CPF_Cliente = %s, Id_Campo = %s, Id_Usuario_Cadastrou = %s
            WHERE Id_Reserva = %s
            RETURNING Id_Reserva, Data, Quant_Horas, Status, CPF_Cliente, Id_Campo, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            reserva.data, reserva.quant_horas, reserva.status,
            reserva.cpf_cliente, reserva.id_campo, reserva.id_usuario_cadastrou, id_reserva
        ))
        
        if result:
            return ReservaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar reserva")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar reserva: {str(e)}")

@router.delete("/{id_reserva}", status_code=204)
async def deletar_reserva(id_reserva: int):
    """Deleta uma reserva"""
    try:
        query_check = "SELECT * FROM Reserva WHERE Id_Reserva = %s"
        existing = db.execute_query(query_check, (id_reserva,))
        if not existing:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        
        query = "DELETE FROM Reserva WHERE Id_Reserva = %s"
        db.execute_query(query, (id_reserva,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar reserva: {str(e)}")

@router.get("/detalhadas", response_model=List[dict])
async def listar_reservas_detalhadas():
    """Lista reservas com detalhes de clientes, campos e usuários via view"""
    try:
        query = "SELECT * FROM view_reservas_detalhadas"
        result = db.execute_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar reservas detalhadas: {str(e)}")
