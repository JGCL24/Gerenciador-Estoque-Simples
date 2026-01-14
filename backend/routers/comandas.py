from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import ComandaCreate, ComandaResponse, ItemComandaCreate, ItemComandaResponse

router = APIRouter()

@router.post("/", response_model=ComandaResponse, status_code=201)
async def criar_comanda(comanda: ComandaCreate):
    """Cria uma nova comanda"""
    try:
        # Verifica se a mesa existe
        query_mesa = "SELECT * FROM Mesa WHERE Numero = %s"
        mesa = db.execute_query(query_mesa, (comanda.numero_mesa,))
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
        
        # Verifica se o cliente existe
        query_cliente = "SELECT * FROM Cliente WHERE CPF = %s"
        cliente = db.execute_query(query_cliente, (comanda.cpf_cliente,))
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Verifica se o funcionário existe
        query_func = "SELECT * FROM Funcionario WHERE Id_Usuario = %s"
        func = db.execute_query(query_func, (comanda.id_funcionario,))
        if not func:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        
        # Verifica se a mesa já está ocupada
        query_mesa_ocupada = "SELECT * FROM Comanda WHERE Numero_Mesa = %s AND Status = 'Aberta'"
        mesa_ocupada = db.execute_query(query_mesa_ocupada, (comanda.numero_mesa,))
        if mesa_ocupada:
            raise HTTPException(status_code=400, detail="Mesa já está ocupada")
        
        # Gera próximo ID de comanda
        query_max = "SELECT COALESCE(MAX(Id_Comanda), 0) + 1 AS next_id FROM Comanda"
        max_result = db.execute_query(query_max)
        next_id = max_result[0]['next_id'] if max_result else 1
        
        query = """
            INSERT INTO Comanda (Id_Comanda, Data, Status, Numero_Mesa, CPF_Cliente, Id_Funcionario)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING Id_Comanda, Data, Status, Numero_Mesa, CPF_Cliente, Id_Funcionario
        """
        result = db.execute_query(query, (
            next_id, comanda.data, comanda.status, comanda.numero_mesa,
            comanda.cpf_cliente, comanda.id_funcionario
        ))
        
        if result:
            # Atualiza status da mesa
            db.execute_query(
                "UPDATE Mesa SET Status = 'Ocupada' WHERE Numero = %s",
                (comanda.numero_mesa,),
                fetch=False
            )
            return ComandaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar comanda")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar comanda: {str(e)}")

@router.get("/", response_model=List[ComandaResponse])
async def listar_comandas():
    """Lista todas as comandas"""
    try:
        query = """
            SELECT Id_Comanda, Data, Status, Numero_Mesa, CPF_Cliente, Id_Funcionario
            FROM Comanda
            ORDER BY Data DESC
        """
        result = db.execute_query(query)
        return [ComandaResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar comandas: {str(e)}")

@router.get("/{id_comanda}", response_model=ComandaResponse)
async def obter_comanda(id_comanda: int):
    """Obtém uma comanda por ID"""
    try:
        query = """
            SELECT Id_Comanda, Data, Status, Numero_Mesa, CPF_Cliente, Id_Funcionario
            FROM Comanda WHERE Id_Comanda = %s
        """
        result = db.execute_query(query, (id_comanda,))
        if not result:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        return ComandaResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter comanda: {str(e)}")

@router.put("/{id_comanda}", response_model=ComandaResponse)
async def atualizar_comanda(id_comanda: int, comanda: ComandaCreate):
    """Atualiza uma comanda"""
    try:
        query_check = "SELECT * FROM Comanda WHERE Id_Comanda = %s"
        existing = db.execute_query(query_check, (id_comanda,))
        if not existing:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        
        query = """
            UPDATE Comanda 
            SET Data = %s, Status = %s, Numero_Mesa = %s, CPF_Cliente = %s, Id_Funcionario = %s
            WHERE Id_Comanda = %s
            RETURNING Id_Comanda, Data, Status, Numero_Mesa, CPF_Cliente, Id_Funcionario
        """
        result = db.execute_query(query, (
            comanda.data, comanda.status, comanda.numero_mesa,
            comanda.cpf_cliente, comanda.id_funcionario, id_comanda
        ))
        
        if result:
            # Se comanda fechada, libera a mesa
            if comanda.status == 'Fechada':
                db.execute_query(
                    "UPDATE Mesa SET Status = 'Livre' WHERE Numero = %s",
                    (comanda.numero_mesa,),
                    fetch=False
                )
            return ComandaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar comanda")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar comanda: {str(e)}")

@router.delete("/{id_comanda}", status_code=204)
async def deletar_comanda(id_comanda: int):
    """Deleta uma comanda"""
    try:
        query_check = "SELECT * FROM Comanda WHERE Id_Comanda = %s"
        existing = db.execute_query(query_check, (id_comanda,))
        if not existing:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        
        # Libera a mesa antes de deletar
        numero_mesa = existing[0]['Numero_Mesa']
        db.execute_query(
            "UPDATE Mesa SET Status = 'Livre' WHERE Numero = %s",
            (numero_mesa,),
            fetch=False
        )
        
        query = "DELETE FROM Comanda WHERE Id_Comanda = %s"
        db.execute_query(query, (id_comanda,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar comanda: {str(e)}")

# Endpoints para Itens de Comanda
@router.post("/{id_comanda}/itens", response_model=ItemComandaResponse, status_code=201)
async def adicionar_item_comanda(id_comanda: int, item: ItemComandaCreate):
    """Adiciona um item a uma comanda"""
    try:
        # Verifica se a comanda existe
        query_comanda = "SELECT * FROM Comanda WHERE Id_Comanda = %s"
        comanda = db.execute_query(query_comanda, (id_comanda,))
        if not comanda:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")
        
        # Verifica se o produto existe
        query_produto = "SELECT * FROM Produto WHERE Id_Produto = %s"
        produto = db.execute_query(query_produto, (item.id_produto,))
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        # Verifica se o item já existe na comanda
        query_check = """
            SELECT * FROM Item_Comanda 
            WHERE Id_Comanda = %s AND Id_Produto = %s
        """
        existing = db.execute_query(query_check, (id_comanda, item.id_produto))
        
        if existing:
            # Atualiza quantidade e preço
            query_update = """
                UPDATE Item_Comanda 
                SET Quantidade = Quantidade + %s, Preco_Unitario = %s
                WHERE Id_Comanda = %s AND Id_Produto = %s
                RETURNING Id_Comanda, Id_Produto, Quantidade, Preco_Unitario
            """
            result = db.execute_query(query_update, (
                item.quantidade, item.preco_unitario, id_comanda, item.id_produto
            ))
        else:
            # Insere novo item
            query_insert = """
                INSERT INTO Item_Comanda (Id_Comanda, Id_Produto, Quantidade, Preco_Unitario)
                VALUES (%s, %s, %s, %s)
                RETURNING Id_Comanda, Id_Produto, Quantidade, Preco_Unitario
            """
            result = db.execute_query(query_insert, (
                id_comanda, item.id_produto, item.quantidade, item.preco_unitario
            ))
        
        if result:
            return ItemComandaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao adicionar item à comanda")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar item: {str(e)}")

@router.get("/{id_comanda}/itens", response_model=List[ItemComandaResponse])
async def listar_itens_comanda(id_comanda: int):
    """Lista todos os itens de uma comanda"""
    try:
        query = """
            SELECT Id_Comanda, Id_Produto, Quantidade, Preco_Unitario
            FROM Item_Comanda
            WHERE Id_Comanda = %s
        """
        result = db.execute_query(query, (id_comanda,))
        return [ItemComandaResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar itens: {str(e)}")

@router.delete("/{id_comanda}/itens/{id_produto}", status_code=204)
async def remover_item_comanda(id_comanda: int, id_produto: int):
    """Remove um item de uma comanda"""
    try:
        query = "DELETE FROM Item_Comanda WHERE Id_Comanda = %s AND Id_Produto = %s"
        db.execute_query(query, (id_comanda, id_produto), fetch=False)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover item: {str(e)}")
