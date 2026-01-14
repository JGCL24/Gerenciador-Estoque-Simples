from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import CompraCreate, CompraResponse, ItemCompraCreate, ItemCompraResponse

router = APIRouter()

@router.post("/", response_model=CompraResponse, status_code=201)
async def criar_compra(compra: CompraCreate):
    """Cria uma nova compra"""
    try:
        # Verifica se o cliente existe
        query_cliente = "SELECT * FROM Cliente WHERE CPF = %s"
        cliente = db.execute_query(query_cliente, (compra.cpf_cliente,))
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        query = """
            INSERT INTO Compra (Data, Valor_Total, CPF_Cliente)
            VALUES (%s, %s, %s)
            RETURNING Id_Compra, Data, Valor_Total, CPF_Cliente, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            compra.data, compra.valor_total, compra.cpf_cliente
        ))
        if result:
            return CompraResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar compra")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar compra: {str(e)}")

@router.get("/", response_model=List[CompraResponse])
async def listar_compras():
    """Lista todas as compras"""
    try:
        query = """
            SELECT Id_Compra, Data, Valor_Total, CPF_Cliente, Id_Usuario_Cadastrou
            FROM Compra
            ORDER BY Data DESC
        """
        result = db.execute_query(query)
        return [CompraResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar compras: {str(e)}")

@router.get("/{id_compra}", response_model=CompraResponse)
async def obter_compra(id_compra: int):
    """Obtém uma compra por ID"""
    try:
        query = """
            SELECT Id_Compra, Data, Valor_Total, CPF_Cliente, Id_Usuario_Cadastrou
            FROM Compra WHERE Id_Compra = %s
        """
        result = db.execute_query(query, (id_compra,))
        if not result:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        return CompraResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter compra: {str(e)}")

@router.get("/cliente/{cpf}", response_model=List[CompraResponse])
async def listar_compras_cliente(cpf: str):
    """Lista todas as compras de um cliente"""
    try:
        query = """
            SELECT Id_Compra, Data, Valor_Total, CPF_Cliente, Id_Usuario_Cadastrou
            FROM Compra WHERE CPF_Cliente = %s
            ORDER BY Data DESC
        """
        result = db.execute_query(query, (cpf,))
        return [CompraResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar compras do cliente: {str(e)}")

@router.put("/{id_compra}", response_model=CompraResponse)
async def atualizar_compra(id_compra: int, compra: CompraCreate):
    """Atualiza uma compra"""
    try:
        query_check = "SELECT * FROM Compra WHERE Id_Compra = %s"
        existing = db.execute_query(query_check, (id_compra,))
        if not existing:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        
        query = """
            UPDATE Compra 
            SET Data = %s, Valor_Total = %s, CPF_Cliente = %s, Id_Usuario_Cadastrou = %s
            WHERE Id_Compra = %s
            RETURNING Id_Compra, Data, Valor_Total, CPF_Cliente, Id_Usuario_Cadastrou
        """
        result = db.execute_query(query, (
            compra.data, compra.valor_total, compra.cpf_cliente,
            compra.id_usuario_cadastrou, id_compra
        ))
        
        if result:
            return CompraResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar compra")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar compra: {str(e)}")

@router.delete("/{id_compra}", status_code=204)
async def deletar_compra(id_compra: int):
    """Deleta uma compra"""
    try:
        query_check = "SELECT * FROM Compra WHERE Id_Compra = %s"
        existing = db.execute_query(query_check, (id_compra,))
        if not existing:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        
        query = "DELETE FROM Compra WHERE Id_Compra = %s"
        db.execute_query(query, (id_compra,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar compra: {str(e)}")

# Endpoints para Itens de Compra
@router.post("/{id_compra}/itens", response_model=ItemCompraResponse, status_code=201)
async def adicionar_item_compra(id_compra: int, item: ItemCompraCreate):
    """Adiciona um item a uma compra"""
    try:
        # Verifica se a compra existe
        query_compra = "SELECT * FROM Compra WHERE Id_Compra = %s"
        compra = db.execute_query(query_compra, (id_compra,))
        if not compra:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        
        # Verifica se o produto existe
        query_produto = "SELECT * FROM Produto WHERE Id_Produto = %s"
        produto = db.execute_query(query_produto, (item.id_produto,))
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        # Verifica se o item já existe na compra
        query_check = """
            SELECT * FROM Item_Compra 
            WHERE Id_Compra = %s AND Id_Produto = %s
        """
        existing = db.execute_query(query_check, (id_compra, item.id_produto))
        
        if existing:
            # Atualiza quantidade e preço
            query_update = """
                UPDATE Item_Compra 
                SET Quantidade = Quantidade + %s, Preco_Unitario = %s
                WHERE Id_Compra = %s AND Id_Produto = %s
                RETURNING Id_Compra, Id_Produto, Quantidade, Preco_Unitario
            """
            result = db.execute_query(query_update, (
                item.quantidade, item.preco_unitario, id_compra, item.id_produto
            ))
        else:
            # Insere novo item
            query_insert = """
                INSERT INTO Item_Compra (Id_Compra, Id_Produto, Quantidade, Preco_Unitario)
                VALUES (%s, %s, %s, %s)
                RETURNING Id_Compra, Id_Produto, Quantidade, Preco_Unitario
            """
            result = db.execute_query(query_insert, (
                id_compra, item.id_produto, item.quantidade, item.preco_unitario
            ))
        
        # Atualiza valor total da compra
        query_total = """
            SELECT SUM(Quantidade * Preco_Unitario) as total
            FROM Item_Compra
            WHERE Id_Compra = %s
        """
        total_result = db.execute_query(query_total, (id_compra,))
        if total_result and total_result[0]['total']:
            total = float(total_result[0]['total'])
            db.execute_query(
                "UPDATE Compra SET Valor_Total = %s WHERE Id_Compra = %s",
                (total, id_compra),
                fetch=False
            )
        
        if result:
            return ItemCompraResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao adicionar item à compra")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar item: {str(e)}")

@router.get("/{id_compra}/itens", response_model=List[ItemCompraResponse])
async def listar_itens_compra(id_compra: int):
    """Lista todos os itens de uma compra"""
    try:
        query = """
            SELECT Id_Compra, Id_Produto, Quantidade, Preco_Unitario
            FROM Item_Compra
            WHERE Id_Compra = %s
        """
        result = db.execute_query(query, (id_compra,))
        return [ItemCompraResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar itens: {str(e)}")

@router.delete("/{id_compra}/itens/{id_produto}", status_code=204)
async def remover_item_compra(id_compra: int, id_produto: int):
    """Remove um item de uma compra"""
    try:
        query = "DELETE FROM Item_Compra WHERE Id_Compra = %s AND Id_Produto = %s"
        db.execute_query(query, (id_compra, id_produto), fetch=False)
        
        # Atualiza valor total da compra
        query_total = """
            SELECT SUM(Quantidade * Preco_Unitario) as total
            FROM Item_Compra
            WHERE Id_Compra = %s
        """
        total_result = db.execute_query(query_total, (id_compra,))
        if total_result and total_result[0]['total']:
            total = float(total_result[0]['total'])
            db.execute_query(
                "UPDATE Compra SET Valor_Total = %s WHERE Id_Compra = %s",
                (total, id_compra),
                fetch=False
            )
        
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover item: {str(e)}")
