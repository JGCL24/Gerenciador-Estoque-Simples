from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import (
    PagamentoCreate, PagamentoResponse,
    PagComandaCreate, PagReservaCreate, PagCompraCreate
)

router = APIRouter()

# Endpoints para Pagamento
@router.post("/", response_model=PagamentoResponse, status_code=201)
async def criar_pagamento(pagamento: PagamentoCreate):
    """Cria um novo pagamento"""
    try:
        query = """
            INSERT INTO Pagamento (Valor, Forma, Tipo_Pagamento)
            VALUES (%s, %s, %s)
            RETURNING Id_Pagamento, Valor, Forma, Tipo_Pagamento, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            pagamento.valor, pagamento.forma, pagamento.tipo_pagamento
        ))
        if result:
            return PagamentoResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar pagamento")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pagamento: {str(e)}")

@router.get("/", response_model=List[PagamentoResponse])
async def listar_pagamentos():
    """Lista todos os pagamentos"""
    try:
        query = """
            SELECT Id_Pagamento, Valor, Forma, Tipo_Pagamento, Id_Usuario_Cadastrou
            FROM Pagamento
            ORDER BY Id_Pagamento DESC
        """
        result = db.execute_query(query)
        return [PagamentoResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pagamentos: {str(e)}")

@router.get("/{id_pagamento}", response_model=PagamentoResponse)
async def obter_pagamento(id_pagamento: int):
    """Obtém um pagamento por ID"""
    try:
        query = """
            SELECT Id_Pagamento, Valor, Forma, Tipo_Pagamento, Id_Usuario_Cadastrou
            FROM Pagamento WHERE Id_Pagamento = %s
        """
        result = db.execute_query(query, (id_pagamento,))
        if not result:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        return PagamentoResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter pagamento: {str(e)}")

@router.put("/{id_pagamento}", response_model=PagamentoResponse)
async def atualizar_pagamento(id_pagamento: int, pagamento: PagamentoCreate):
    """Atualiza um pagamento"""
    try:
        query_check = "SELECT * FROM Pagamento WHERE Id_Pagamento = %s"
        existing = db.execute_query(query_check, (id_pagamento,))
        if not existing:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        query = """
            UPDATE Pagamento 
            SET Valor = %s, Forma = %s, Tipo_Pagamento = %s, Id_Usuario_Cadastrou = %s
            WHERE Id_Pagamento = %s
            RETURNING Id_Pagamento, Valor, Forma, Tipo_Pagamento, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            pagamento.valor, pagamento.forma, pagamento.tipo_pagamento,
            pagamento.id_usuario_cadastrou, id_pagamento
        ))
        
        if result:
            return PagamentoResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar pagamento")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pagamento: {str(e)}")

@router.delete("/{id_pagamento}", status_code=204)
async def deletar_pagamento(id_pagamento: int):
    """Deleta um pagamento"""
    try:
        query_check = "SELECT * FROM Pagamento WHERE Id_Pagamento = %s"
        existing = db.execute_query(query_check, (id_pagamento,))
        if not existing:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        query = "DELETE FROM Pagamento WHERE Id_Pagamento = %s"
        db.execute_query(query, (id_pagamento,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar pagamento: {str(e)}")

# Endpoint para Pagamento de Comanda
@router.post("/comanda", status_code=201)
async def criar_pagamento_comanda(pag_comanda: PagComandaCreate):
    """Cria um pagamento para uma comanda"""
    try:
        # Verifica se a comanda existe
        query_comanda = "SELECT * FROM Comanda WHERE Id_Comanda = %s"
        comanda = db.execute_query(query_comanda, (pag_comanda.id_comanda,))
        if not comanda:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        
        # Verifica se o pagamento existe
        query_pagamento = "SELECT * FROM Pagamento WHERE Id_Pagamento = %s"
        pagamento = db.execute_query(query_pagamento, (pag_comanda.id_pagamento,))
        if not pagamento:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        # Verifica se já existe pagamento para esta comanda
        query_check = "SELECT * FROM Pag_Comanda WHERE Id_Comanda = %s"
        existing = db.execute_query(query_check, (pag_comanda.id_comanda,))
        if existing:
            raise HTTPException(status_code=400, detail="Comanda já possui pagamento")
        
        query = """
            INSERT INTO Pag_Comanda (Id_Pagamento, Id_Comanda)
            VALUES (%s, %s)
            RETURNING Id_Pagamento, Id_Comanda
        """
        result = db.execute_query(query, (pag_comanda.id_pagamento, pag_comanda.id_comanda))
        
        if result:
            # Atualiza status da comanda para "Paga"
            db.execute_query(
                "UPDATE Comanda SET Status = 'Paga' WHERE Id_Comanda = %s",
                (pag_comanda.id_comanda,),
                fetch=False
            )
            return {"message": "Pagamento de comanda criado com sucesso", "data": result[0]}
        raise HTTPException(status_code=500, detail="Erro ao criar pagamento de comanda")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pagamento de comanda: {str(e)}")

# Endpoint para Pagamento de Reserva
@router.post("/reserva", status_code=201)
async def criar_pagamento_reserva(pag_reserva: PagReservaCreate):
    """Cria um pagamento para uma reserva"""
    try:
        # Verifica se a reserva existe
        query_reserva = "SELECT * FROM Reserva WHERE Id_Reserva = %s"
        reserva = db.execute_query(query_reserva, (pag_reserva.id_reserva,))
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        
        # Verifica se o pagamento existe
        query_pagamento = "SELECT * FROM Pagamento WHERE Id_Pagamento = %s"
        pagamento = db.execute_query(query_pagamento, (pag_reserva.id_pagamento,))
        if not pagamento:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        # Verifica se já existe pagamento para esta reserva
        query_check = "SELECT * FROM Pag_Reserva WHERE Id_Reserva = %s"
        existing = db.execute_query(query_check, (pag_reserva.id_reserva,))
        if existing:
            raise HTTPException(status_code=400, detail="Reserva já possui pagamento")
        
        query = """
            INSERT INTO Pag_Reserva (Id_Pagamento, Id_Reserva, CPF_Cliente, Porcentagem)
            VALUES (%s, %s, %s, %s)
            RETURNING Id_Pagamento, Id_Reserva, CPF_Cliente, Porcentagem
        """
        result = db.execute_query(query, (
            pag_reserva.id_pagamento, pag_reserva.id_reserva,
            pag_reserva.cpf_cliente, pag_reserva.porcentagem
        ))
        
        if result:
            return {"message": "Pagamento de reserva criado com sucesso", "data": result[0]}
        raise HTTPException(status_code=500, detail="Erro ao criar pagamento de reserva")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pagamento de reserva: {str(e)}")

# Endpoint para Pagamento de Compra
@router.post("/compra", status_code=201)
async def criar_pagamento_compra(pag_compra: PagCompraCreate):
    """Cria um pagamento para uma compra"""
    try:
        # Verifica se a compra existe
        query_compra = "SELECT * FROM Compra WHERE Id_Compra = %s"
        compra = db.execute_query(query_compra, (pag_compra.id_compra,))
        if not compra:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        
        # Verifica se o pagamento existe
        query_pagamento = "SELECT * FROM Pagamento WHERE Id_Pagamento = %s"
        pagamento = db.execute_query(query_pagamento, (pag_compra.id_pagamento,))
        if not pagamento:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        
        # Verifica se já existe pagamento para esta compra
        query_check = "SELECT * FROM Pag_Compra WHERE Id_Compra = %s"
        existing = db.execute_query(query_check, (pag_compra.id_compra,))
        if existing:
            raise HTTPException(status_code=400, detail="Compra já possui pagamento")
        
        query = """
            INSERT INTO Pag_Compra (Id_Pagamento, Id_Compra)
            VALUES (%s, %s)
            RETURNING Id_Pagamento, Id_Compra
        """
        result = db.execute_query(query, (pag_compra.id_pagamento, pag_compra.id_compra))
        
        if result:
            return {"message": "Pagamento de compra criado com sucesso", "data": result[0]}
        raise HTTPException(status_code=500, detail="Erro ao criar pagamento de compra")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pagamento de compra: {str(e)}")
