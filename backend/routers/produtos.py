from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from schemas import ProdutoCreate, ProdutoResponse

router = APIRouter()

@router.post("/", response_model=ProdutoResponse, status_code=201)
async def criar_produto(produto: ProdutoCreate):
    """Cria um novo produto"""
    try:
        # Verifica se o admin existe
        query_admin = "SELECT * FROM Administrador WHERE Id_Usuario = %s"
        admin = db.execute_query(query_admin, (produto.id_admin_cadastrou,))
        if not admin:
            raise HTTPException(status_code=404, detail="Administrador não encontrado")
        
        # Gera próximo ID de produto
        query_max = "SELECT COALESCE(MAX(Id_Produto), 0) + 1 AS next_id FROM Produto"
        max_result = db.execute_query(query_max)
        next_id = max_result[0]['next_id'] if max_result else 1
        
        query = """
            INSERT INTO Produto (Id_Produto, Nome, Preco, Validade, Quant_Min_Estoque, Id_Admin_Cadastrou)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING Id_Produto, Nome, Preco, Validade, Quant_Min_Estoque, Id_Admin_Cadastrou
        """
        result = db.execute_query(query, (
            next_id, produto.nome, produto.preco, produto.validade,
            produto.quant_min_estoque, produto.id_admin_cadastrou
        ))
        
        if result:
            return ProdutoResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao criar produto")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")

@router.get("/", response_model=List[ProdutoResponse])
async def listar_produtos():
    """Lista todos os produtos"""
    try:
        query = """
            SELECT Id_Produto, Nome, Preco, Validade, Quant_Min_Estoque, Id_Admin_Cadastrou
            FROM Produto
            ORDER BY Nome
        """
        result = db.execute_query(query)
        return [ProdutoResponse(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")

@router.get("/{id_produto}", response_model=ProdutoResponse)
async def obter_produto(id_produto: int):
    """Obtém um produto por ID"""
    try:
        query = """
            SELECT Id_Produto, Nome, Preco, Validade, Quant_Min_Estoque, Id_Admin_Cadastrou
            FROM Produto WHERE Id_Produto = %s
        """
        result = db.execute_query(query, (id_produto,))
        if not result:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return ProdutoResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter produto: {str(e)}")

@router.put("/{id_produto}", response_model=ProdutoResponse)
async def atualizar_produto(id_produto: int, produto: ProdutoCreate):
    """Atualiza um produto"""
    try:
        query_check = "SELECT * FROM Produto WHERE Id_Produto = %s"
        existing = db.execute_query(query_check, (id_produto,))
        if not existing:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        query = """
            UPDATE Produto 
            SET Nome = %s, Preco = %s, Validade = %s, Quant_Min_Estoque = %s, Id_Admin_Cadastrou = %s
            WHERE Id_Produto = %s
            RETURNING Id_Produto, Nome, Preco, Validade, Quant_Min_Estoque, Id_Admin_Cadastrou
        """
        result = db.execute_query(query, (
            produto.nome, produto.preco, produto.validade,
            produto.quant_min_estoque, produto.id_admin_cadastrou, id_produto
        ))
        
        if result:
            return ProdutoResponse(**result[0])
        raise HTTPException(status_code=500, detail="Erro ao atualizar produto")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {str(e)}")

@router.delete("/{id_produto}", status_code=204)
async def deletar_produto(id_produto: int):
    """Deleta um produto"""
    try:
        query_check = "SELECT * FROM Produto WHERE Id_Produto = %s"
        existing = db.execute_query(query_check, (id_produto,))
        if not existing:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        query = "DELETE FROM Produto WHERE Id_Produto = %s"
        db.execute_query(query, (id_produto,), fetch=False)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar produto: {str(e)}")
