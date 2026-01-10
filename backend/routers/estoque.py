from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import EstoqueCreate, EstoqueResponse, MovimentaCreate, MovimentaResponse

router = APIRouter()

# Endpoints para Estoque
@router.post("/", response_model=EstoqueResponse, status_code=201)
async def criar_estoque(estoque: EstoqueCreate):
    """Cria um novo registro de estoque"""
    try:
        # Verifica se já existe estoque para este produto
        query_check = "SELECT * FROM Estoque WHERE Id_Produto = %s"
        existing = db.execute_query(query_check, (estoque.id_produto,))
        if existing:
            raise HTTPException(status_code=400, detail="Estoque para este produto já existe")
        
        # Verifica se o produto existe
        query_produto = "SELECT * FROM Produto WHERE Id_Produto = %s"
        produto = db.execute_query(query_produto, (estoque.id_produto,))
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        # Gera próximo ID de estoque
        query_max = "SELECT COALESCE(MAX(Id_Estoque), 0) + 1 AS next_id FROM Estoque"
        max_result = db.execute_query(query_max)
        next_id = max_result[0]['next_id'] if max_result else 1
        
        query = """
            INSERT INTO Estoque (Id_Estoque, Id_Produto, Quant_Present)
            VALUES (%s, %s, %s)
            RETURNING Id_Estoque, Id_Produto, Quant_Present
        """
        result = db.execute_query(query, (next_id, estoque.id_produto, estoque.quant_present))
        
        if result:
            return EstoqueResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar estoque")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar estoque: {str(e)}")

@router.get("/", response_model=List[EstoqueResponse])
async def listar_estoques():
    """Lista todos os estoques"""
    try:
        query = "SELECT Id_Estoque, Id_Produto, Quant_Present FROM Estoque"
        result = db.execute_query(query)
        return [EstoqueResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar estoques: {str(e)}")

@router.get("/produto/{id_produto}", response_model=EstoqueResponse)
async def obter_estoque_produto(id_produto: int):
    """Obtém o estoque de um produto"""
    try:
        query = "SELECT Id_Estoque, Id_Produto, Quant_Present FROM Estoque WHERE Id_Produto = %s"
        result = db.execute_query(query, (id_produto,))
        if not result:
            raise HTTPException(status_code=404, detail="Estoque não encontrado para este produto")
        return EstoqueResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estoque: {str(e)}")

@router.put("/produto/{id_produto}", response_model=EstoqueResponse)
async def atualizar_estoque(id_produto: int, estoque: EstoqueCreate):
    """Atualiza o estoque de um produto"""
    try:
        query_check = "SELECT * FROM Estoque WHERE Id_Produto = %s"
        existing = db.execute_query(query_check, (id_produto,))
        if not existing:
            raise HTTPException(status_code=404, detail="Estoque não encontrado")
        
        query = """
            UPDATE Estoque 
            SET Quant_Present = %s
            WHERE Id_Produto = %s
            RETURNING Id_Estoque, Id_Produto, Quant_Present
        """
        result = db.execute_query(query, (estoque.quant_present, id_produto))
        
        if result:
            return EstoqueResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar estoque")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar estoque: {str(e)}")

# Endpoints para Movimentações
@router.post("/movimentacoes", response_model=MovimentaResponse, status_code=201)
async def criar_movimentacao(movimenta: MovimentaCreate):
    """Cria uma nova movimentação de estoque"""
    try:
        # Verifica se o estoque existe
        query_estoque = "SELECT * FROM Estoque WHERE Id_Estoque = %s"
        estoque = db.execute_query(query_estoque, (movimenta.id_estoque,))
        if not estoque:
            raise HTTPException(status_code=404, detail="Estoque não encontrado")
        
        # Atualiza a quantidade presente no estoque
        if movimenta.tipo.lower() == "entrada":
            query_update = """
                UPDATE Estoque 
                SET Quant_Present = Quant_Present + %s
                WHERE Id_Estoque = %s
            """
        elif movimenta.tipo.lower() == "saida":
            query_update = """
                UPDATE Estoque 
                SET Quant_Present = Quant_Present - %s
                WHERE Id_Estoque = %s
            """
        else:
            raise HTTPException(status_code=400, detail="Tipo de movimentação inválido. Use 'entrada' ou 'saida'")
        
        db.execute_query(query_update, (movimenta.quantidade, movimenta.id_estoque), fetch=False)
        
        # Gera próximo ID de movimentação
        query_max = "SELECT COALESCE(MAX(Id_Movimenta), 0) + 1 AS next_id FROM Movimenta"
        max_result = db.execute_query(query_max)
        next_id = max_result[0]['next_id'] if max_result else 1
        
        query = """
            INSERT INTO Movimenta (Id_Movimenta, Id_Estoque, Tipo, Quantidade, Data)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING Id_Movimenta, Id_Estoque, Tipo, Quantidade, Data
        """
        result = db.execute_query(query, (
            next_id, movimenta.id_estoque, movimenta.tipo,
            movimenta.quantidade, movimenta.data
        ))
        
        if result:
            return MovimentaResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar movimentação")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar movimentação: {str(e)}")

@router.get("/movimentacoes", response_model=List[MovimentaResponse])
async def listar_movimentacoes():
    """Lista todas as movimentações"""
    try:
        query = """
            SELECT Id_Movimenta, Id_Estoque, Tipo, Quantidade, Data
            FROM Movimenta
            ORDER BY Data DESC
        """
        result = db.execute_query(query)
        return [MovimentaResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar movimentações: {str(e)}")

@router.get("/movimentacoes/{id_movimenta}", response_model=MovimentaResponse)
async def obter_movimentacao(id_movimenta: int):
    """Obtém uma movimentação por ID"""
    try:
        query = """
            SELECT Id_Movimenta, Id_Estoque, Tipo, Quantidade, Data
            FROM Movimenta WHERE Id_Movimenta = %s
        """
        result = db.execute_query(query, (id_movimenta,))
        if not result:
            raise HTTPException(status_code=404, detail="Movimentação não encontrada")
        return MovimentaResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter movimentação: {str(e)}")
