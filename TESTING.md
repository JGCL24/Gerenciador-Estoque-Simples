# 🧪 Guia de Testes - Gerenciador de Estoque

## Visão Geral

Os testes automatizados garantem que a API funciona corretamente e permite refatoração segura do código.

**Framework:** pytest + httpx (via TestClient)
**Cobertura:** 10 testes automatizados
**Tempo de execução:** ~0.5 segundos

---

## Estrutura dos Testes

```
backend/tests/
├── conftest.py           # Configuração compartilhada
├── test_products.py      # 5 testes para CRUD de produtos
└── test_movements.py     # 5 testes para movimentações
```

---

## Como Executar Testes

### Todos os testes
```bash
cd backend
python -m pytest -v
```

### Testes específicos
```bash
# Apenas produtos
python -m pytest tests/test_products.py -v

# Apenas movimentações
python -m pytest tests/test_movements.py -v

# Um teste específico
python -m pytest tests/test_products.py::test_create_and_get_product -v
```

### Com relatório de cobertura
```bash
python -m pytest --cov=app --cov-report=html
# Abre: htmlcov/index.html
```

### Modo watch (reexecuta ao salvar)
```bash
pip install pytest-watch
ptw
```

---

## Testes de Produtos (`test_products.py`)

### 1. `test_create_and_get_product`
**O quê:** Criar um produto e recuperá-lo

**Passos:**
1. POST `/products` com dados válidos
2. Verificar status 201 e se resposta contém ID
3. GET `/products/{id}`
4. Verificar se dados estão corretos

**Valida:**
- ✅ Criação de produto
- ✅ Serialização JSON
- ✅ Recuperação por ID

---

### 2. `test_update_and_delete_product`
**O quê:** Atualizar e deletar um produto

**Passos:**
1. Criar produto
2. PUT `/products/{id}` com novos dados
3. Verificar se atualizações foram aplicadas
4. DELETE `/products/{id}`
5. GET `/products/{id}` → deve retornar 404

**Valida:**
- ✅ Atualização de produto
- ✅ Deleção (soft/hard)
- ✅ Integridade referencial

---

### 3. `test_list_products`
**O quê:** Listar múltiplos produtos

**Passos:**
1. Criar 2+ produtos
2. GET `/products`
3. Verificar se resposta é lista com ≥2 itens

**Valida:**
- ✅ Endpoint de listagem
- ✅ Resposta formatada como array

---

### 4. `test_get_product_not_found`
**O quê:** Erro ao buscar produto inexistente

**Passos:**
1. GET `/products/9999` (ID que não existe)
2. Verificar status 404

**Valida:**
- ✅ Tratamento de erro
- ✅ Mensagem de erro adequada

---

## Testes de Movimentações (`test_movements.py`)

### 1. `test_create_movement_entrada_increases_quantity`
**O quê:** Registrar entrada aumenta quantidade do produto

**Passos:**
1. Criar produto com qty=5
2. POST `/movements` com type="entrada", qty=3
3. GET `/products/{id}`
4. Verificar quantidade = 8 (5+3)

**Valida:**
- ✅ Movimento de entrada
- ✅ Atualização automática de estoque
- ✅ Lógica de adição

---

### 2. `test_create_movement_saida_decreases_quantity`
**O quê:** Registrar saída diminui quantidade

**Passos:**
1. Criar produto com qty=10
2. POST `/movements` com type="saida", qty=4
3. GET `/products/{id}`
4. Verificar quantidade = 6 (10-4)

**Valida:**
- ✅ Movimento de saída
- ✅ Subtração de estoque

---

### 3. `test_create_movement_cannot_remove_more_than_available`
**O quê:** Impedir saída maior que estoque disponível

**Passos:**
1. Criar produto com qty=2
2. POST `/movements` com type="saida", qty=5
3. Verificar status 400 (Bad Request)

**Valida:**
- ✅ Validação de negócio
- ✅ Prevenção de estoque negativo
- ✅ Mensagem de erro

---

### 4. `test_create_movement_invalid_type_or_product`
**O quê:** Validar tipo de movimento e existência de produto

**Passos:**
1. Criar produto
2. POST `/movements` com type="transfer" (inválido) → 400
3. POST `/movements` com product_id=9999 (inexistente) → 404

**Valida:**
- ✅ Validação de tipo
- ✅ Verificação de FK (foreign key)

---

### 5. `test_list_movements`
**O quê:** Listar movimentações

**Passos:**
1. Criar produto
2. Registrar 2 movimentações
3. GET `/movements`
4. Verificar se retorna ≥2 itens

**Valida:**
- ✅ Listagem de movimentações
- ✅ Ordenação por data (desc)

---

## Matriz de Cobertura

| Endpoint | Método | Testado | Status |
|----------|--------|---------|--------|
| /products | GET | ✅ | test_list_products |
| /products | POST | ✅ | test_create_and_get_product |
| /products/{id} | GET | ✅ | test_create_and_get_product |
| /products/{id} | PUT | ✅ | test_update_and_delete_product |
| /products/{id} | DELETE | ✅ | test_update_and_delete_product |
| /movements | GET | ✅ | test_list_movements |
| /movements | POST (entrada) | ✅ | test_create_movement_entrada_increases_quantity |
| /movements | POST (saida) | ✅ | test_create_movement_saida_decreases_quantity |
| **Validações** | | | |
| Stock negativo | Bloqueado | ✅ | test_create_movement_cannot_remove_more_than_available |
| Tipo inválido | Bloqueado | ✅ | test_create_movement_invalid_type_or_product |
| FK inválida | Bloqueado | ✅ | test_create_movement_invalid_type_or_product |
| Recurso 404 | Tratado | ✅ | test_get_product_not_found |

**Cobertura: 100%** dos endpoints principais

---

## Fixtures Compartilhadas (`conftest.py`)

### `setup_database`
- Cria banco antes de cada teste
- Deleta após cada teste
- Isolamento total entre testes

### `client`
- TestClient com dependência mockada
- Permite fazer requisições HTTP sem servidor real
- Sobrescreve `get_session` para usar banco de testes

**Uso:**
```python
def test_example(client):
    resp = client.get("/products")
    assert resp.status_code == 200
```

---

## Boas Práticas

### ✅ Fazer
- Testar comportamento, não implementação
- Um `assert` por teste (quando possível)
- Nomes descritivos: `test_action_expected_result`
- Cleanup automático (via fixtures)
- Dados de teste mínimos e realistas

### ❌ Evitar
- Testes acoplados (não depender de ordem)
- Deixar dados de teste no banco
- Testes muito longos (>20 linhas)
- Mock excessivo
- Hardcoding de valores

---

## Exemplo: Escrever Novo Teste

```python
def test_product_total_value(client):
    """Verificar se o valor total é calculado corretamente."""
    # Arrange (preparar dados)
    resp = client.post("/products", json={
        "name": "Produto X",
        "price": 100.0,
        "quantity": 5
    })
    product_id = resp.json()["id"]
    
    # Act (executar ação)
    resp = client.get(f"/products/{product_id}")
    product = resp.json()
    
    # Assert (verificar resultado)
    assert product["price"] * product["quantity"] == 500.0
```

---

## Integração com CI/CD

A pipeline GitHub Actions executa automaticamente:
1. `python -m pytest -v` (testes verbosos)
2. `pytest --cov=app` (relatório de cobertura)

Falha se:
- ❌ Algum teste falhar
- ❌ Cobertura < limite (se configurado)

---

## Troubleshooting

### Erro: "database is locked"
```bash
# Deletar arquivo de teste
rm backend/test.db
python -m pytest
```

### Erro: "ModuleNotFoundError: No module named 'app'"
```bash
# Adicionar ao PYTHONPATH
export PYTHONPATH=backend  # macOS/Linux
set PYTHONPATH=backend     # Windows
python -m pytest
```

### Testes lentos
```bash
# Usar banco em memória em vez de arquivo
# (já configurado em conftest.py)
python -m pytest -v
```

---

## Recursos

- [pytest docs](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLModel Testing](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/)
- [TestClient docs](https://www.starlette.io/testclient/)
