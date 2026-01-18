# 🧾 Gerenciador de Estoque

Um sistema completo de gestão de estoque com **backend robusto em FastAPI** e **interface moderna em React**.

**Stack:** FastAPI + SQLModel + SQLite | React + Vite | GitHub Actions CI/CD

---

## 📋 Índice

1. [Visão Geral](#-visão-geral)
2. [Arquitetura do Projeto](#-arquitetura-do-projeto)
3. [Pré-requisitos](#-pré-requisitos)
4. [Instalação e Setup](#-instalação-e-setup)
5. [Como Executar](#-como-executar)
6. [API REST Endpoints](#-api-rest-endpoints)
7. [Testes Automatizados](#-testes-automatizados)
8. [Pipeline CI/CD](#-pipeline-cicd)
9. [Estrutura de Arquivos](#-estrutura-de-arquivos)
10. [Funcionalidades Principais](#-funcionalidades-principais)

---

## 🎯 Visão Geral

**Gerenciador de Estoque** é uma solução de código aberto para gerenciar inventário de produtos com rastreamento completo de movimentações (entradas e saídas).

### Principais Recursos:
- ✅ **CRUD de Produtos** - Criar, ler, atualizar e deletar produtos
- ✅ **Movimentações de Estoque** - Registrar entradas e saídas com histórico completo
- ✅ **Alertas de Estoque Baixo** - Avisos quando quantidade mínima é atingida
- ✅ **Resumo Financeiro** - Total de itens e valor total em estoque
- ✅ **Histórico de Movimentações** - Rastreamento completo com datas
- ✅ **Interface Responsiva** - Funciona em desktop e mobile
- ✅ **API REST Completa** - Integração fácil com outros sistemas

---

## 🏗️ Arquitetura do Projeto

```
Gerenciador-Estoque/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py            # Rotas principais (Products, Movements)
│   │   ├── models.py          # Modelos SQLModel (Product, Movement)
│   │   ├── database.py        # Configuração SQLite e sessões
│   │   └── __pycache__/       # Cache Python (ignorado)
│   ├── tests/
│   │   ├── conftest.py        # Configuração pytest
│   │   ├── test_products.py   # Testes CRUD de produtos
│   │   └── test_movements.py  # Testes de movimentações
│   ├── requirements.txt        # Dependências Python
│   ├── run.py                 # Script para iniciar servidor
│   └── database.db            # Banco SQLite (gerado automaticamente)
│
├── frontend/                   # React + Vite SPA
│   ├── src/
│   │   ├── api.js             # Cliente HTTP para API
│   │   ├── App.jsx            # Componente raiz
│   │   ├── main.jsx           # Entrada React
│   │   ├── styles.css         # Estilos globais
│   │   └── components/
│   │       ├── ProductList.jsx
│   │       ├── MovementsCard.jsx
│   │       ├── Summary.jsx
│   │       ├── ProductForm.jsx
│   │       ├── MovementForm.jsx
│   │       ├── SalesForm.jsx
│   │       └── modals/        # Modal dialogs
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── .github/workflows/
│   └── ci.yml                 # Pipeline CI/CD GitHub Actions
│
├── .gitignore
└── README.md                  # Este arquivo
```

---

## ⚙️ Pré-requisitos

- **Python 3.10+** (testado em 3.10 e 3.11)
- **pip** (gerenciador de pacotes Python)
- **Node.js 16+** (LTS recomendado)
- **npm** (vem com Node.js)
- **Git** (para controle de versão)

### Verificar instalação:
```bash
python --version      # Python 3.10+
pip --version
node --version        # Node 16+
npm --version
git --version
```

---

## 🚀 Instalação e Setup

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/Gerenciador-Estoque.git
cd Gerenciador-Estoque
```

### 2. Setup do Backend

#### Windows (PowerShell)
```powershell
cd backend

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Se houver erro de execução, use:
# powershell -ExecutionPolicy Bypass -File .\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

#### macOS / Linux (Bash)
```bash
cd backend

# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Setup do Frontend

```bash
cd frontend

# Instalar dependências
npm install

# (Opcional) Adicionar dependências específicas se necessário
# npm install axios
```

---

## ▶️ Como Executar

### Opção 1: Backend e Frontend Separados

#### Terminal 1 - Backend
```bash
cd backend

# Windows
.\.venv\Scripts\Activate.ps1
python run.py

# macOS/Linux
source .venv/bin/activate
python run.py
```

Saída esperada:
```
App: http://localhost:8000
Docs: http://localhost:8000/docs
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Saída esperada:
```
Local:   http://localhost:5173/
```

Acesse: **http://localhost:5173/**

---

## 📡 API REST Endpoints

### Base URL: `http://localhost:8000`

### 🛍️ Produtos (`/products`)

| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| `GET` | `/products` | Listar todos os produtos | 200 |
| `POST` | `/products` | Criar novo produto | 201 |
| `GET` | `/products/{id}` | Obter produto específico | 200 |
| `PUT` | `/products/{id}` | Atualizar produto | 200 |
| `DELETE` | `/products/{id}` | Deletar produto | 204 |

#### Exemplo - Criar Produto:
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Notebook",
    "description": "Laptop 15 polegadas",
    "price": 2999.99,
    "quantity": 5,
    "min_quantity": 1
  }'
```

**Resposta (201):**
```json
{
  "id": 1,
  "name": "Notebook",
  "description": "Laptop 15 polegadas",
  "price": 2999.99,
  "quantity": 5,
  "min_quantity": 1
}
```

---

### 📦 Movimentações (`/movements`)

| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| `GET` | `/movements` | Listar movimentações (desc. por data) | 200 |
| `POST` | `/movements` | Criar movimentação (entrada/saída) | 201 |

#### Exemplo - Registrar Entrada:
```bash
curl -X POST http://localhost:8000/movements \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "type": "entrada",
    "quantity": 3,
    "note": "Reabastecimento - Fornecedor X"
  }'
```

**Resposta (201):**
```json
{
  "id": 1,
  "product_id": 1,
  "type": "entrada",
  "quantity": 3,
  "note": "Reabastecimento - Fornecedor X",
  "timestamp": "2026-01-17T10:30:00"
}
```

### Tipos de Movimentação:
- `"entrada"` - Aumenta a quantidade
- `"saida"` - Diminui a quantidade

---

## 🧪 Testes Automatizados

Os testes garantem que a API funciona conforme especificado.

### Executar Testes

```bash
cd backend

# Todos os testes
python -m pytest -v

# Testes específicos
python -m pytest tests/test_products.py -v
python -m pytest tests/test_movements.py -v

# Com cobertura de código
python -m pytest --cov=app --cov-report=html
```

### Suites de Teste

#### `test_products.py` (5 testes)
- ✅ `test_create_and_get_product` - Criar e recuperar produto
- ✅ `test_update_and_delete_product` - Atualizar e deletar
- ✅ `test_list_products` - Listar produtos
- ✅ `test_get_product_not_found` - Erro 404

#### `test_movements.py` (5 testes)
- ✅ `test_create_movement_entrada_increases_quantity` - Entrada aumenta qtd
- ✅ `test_create_movement_saida_decreases_quantity` - Saída diminui qtd
- ✅ `test_create_movement_cannot_remove_more_than_available` - Validação de estoque
- ✅ `test_create_movement_invalid_type_or_product` - Validação de tipo
- ✅ `test_list_movements` - Listar movimentações

**Total: 10 testes** cobrindo todos os endpoints principais.

### O que é Testado:
- ✓ Criação e validação de produtos
- ✓ CRUD completo (Create, Read, Update, Delete)
- ✓ Movimentações de estoque (entrada/saída)
- ✓ Validações de negócio (não permitir saída maior que estoque)
- ✓ Tratamento de erros (404, 400)
- ✓ Integridade de dados no banco

---

## 🔄 Pipeline CI/CD

A pipeline GitHub Actions automatiza testes e build a cada commit.

### O que faz a Pipeline:

```mermaid
[Push/PR] 
    ↓
[Backend Tests (3.10 & 3.11)]
    ↓
[Frontend Build]
    ↓
[Summary - Sucesso/Falha]
```

### Configuração (`.github/workflows/ci.yml`)

1. **Backend Tests (backend-tests)**
   - Roda em Python 3.10 e 3.11
   - Executa: `pytest -v`
   - Gera relatório de cobertura
   - Cache de dependências pip

2. **Frontend Build (frontend-build)**
   - Roda após backend passar
   - Executa: `npm run build`
   - Cache de dependências npm

3. **Summary**
   - Verifica se tudo passou
   - Retorna status geral da pipeline

### Triggers:
- ✅ Push em `main`, `master`, `develop`
- ✅ Pull Requests em `main`, `master`, `develop`

### Status da Pipeline:
Veja o status em: **Aba "Actions"** do repositório GitHub

---

## 📁 Estrutura de Arquivos

### Backend

**`app/models.py`** - Modelos de Dados
```python
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float = 0.0
    quantity: int = 0
    min_quantity: int = 0

class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    type: str  # 'entrada' ou 'saida'
    quantity: int
    note: Optional[str] = None
    timestamp: datetime
```

**`app/main.py`** - API Endpoints
- Rotas em `/products` (CRUD)
- Rotas em `/movements` (entrada/saída)
- Middleware CORS habilitado
- Suporte a SQLite

**`app/database.py`** - Configuração do Banco
- Conexão SQLite
- Session management
- Criação automática de tabelas

**`requirements.txt`** - Dependências
```
fastapi          # Framework web
uvicorn          # Servidor ASGI
sqlmodel         # ORM (SQL + Pydantic)
python-multipart # Upload de arquivos
python-dotenv    # Variáveis de ambiente
pytest           # Framework de testes
httpx            # Cliente HTTP para testes
```

### Frontend

**`src/api.js`** - Cliente HTTP
- Funções para CRUD de produtos
- Funções para movimentações
- Integração com backend

**`src/components/`** - Componentes React
- `ProductList.jsx` - Grade/tabela de produtos
- `MovementsCard.jsx` - Card com últimas movimentações
- `Summary.jsx` - Resumo (total itens, valor)
- `ProductForm.jsx` - Formulário CRUD
- `MovementForm.jsx` - Formulário de movimentações
- Modals para dialogs

---

## ✨ Funcionalidades Principais

### 1️⃣ Gestão de Produtos
- Criar, editar e deletar produtos
- Campos: Nome, Descrição, Preço, Quantidade, Quantidade Mínima
- Validação de dados em tempo real

### 2️⃣ Movimentações de Estoque
- Registrar **entradas** (reabastecimento)
- Registrar **saídas** (vendas, devolução)
- Histórico completo com datas
- Modal para visualizar detalhes

### 3️⃣ Alertas de Estoque Baixo
- Avisos quando qtd < mínima
- Ação rápida para adicionar estoque
- Painel destacado

### 4️⃣ Resumo Financeiro
- Total de itens em estoque
- Valor total em estoque
- Atualização em tempo real

### 5️⃣ Interface Intuitiva
- Design limpo e moderno
- Responsivo (mobile/desktop)
- Validações cliente-servidor
- Feedback de erros claro

---

## 🔧 Variáveis de Ambiente

### Backend (`backend/.env`)
```
DATABASE_URL=sqlite:///./database.db
HOST=0.0.0.0
PORT=8000
```

### Frontend (`frontend/.env`)
```
VITE_API_URL=http://localhost:8000
```

---

## 📚 Documentação Interativa da API

Após iniciar o backend, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona minha feature'`)
4. Push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

---

## 🆘 Troubleshooting

### Backend não conecta ao banco
```bash
# Deletar banco corrompido (data será perdida)
rm database.db
python run.py
```

### Porta 8000 já está em uso
```bash
# Mudar porta
PORT=8001 python run.py
```

### Node modules corrompido
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Testes falhando
```bash
cd backend
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
python -m pytest -v
```

---

## 📞 Suporte

Para dúvidas ou bugs, abra uma issue no GitHub.

**Última atualização:** 17 de Janeiro de 2026

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py

# Em outro terminal, Frontend
cd frontend
npm install
npm run dev
```

Abra o frontend em: `http://localhost:5173` (por padrão) e a API em `http://localhost:8000`.

---

## 🖥️ Backend (FastAPI)
- Iniciar (desenvolvimento): `python run.py` — o script mostra os links da app e da documentação (Swagger: `/docs`).
- Banco padrão: `backend/database.db` (SQLite).
- Migração do campo `min_quantity`: o backend tenta adicionar automaticamente essa coluna em bases antigas; em ambiente de desenvolvimento, apagar `backend/database.db` recria o schema caso necessário.
- Checagem rápida de dependências Python: `python check_prereqs.py` (dentro de `backend/`).

---

## 🌐 Frontend (Vite + React)
- Inicie em `frontend/` com `npm install` e `npm run dev`.
- Configure a URL da API criando `frontend/.env` a partir de `frontend/.env.example` (variável `VITE_API_URL`).

---

## ⚠️ Observações importantes
- CORS já está configurado para o frontend `http://localhost:5173`.
- Se algo não funcionar (ex.: migrations), tente apagar `backend/database.db` e reiniciar a API (apenas em desenvolvimento).

---

## 🛠️ Scripts úteis
- `scripts/check_prereqs.ps1` — checa Python / Node / npm (Windows PowerShell).
- `scripts/check_prereqs.sh` — checa Python / Node / npm (macOS / Linux).
- `backend/check_prereqs.py` — checa se os pacotes Python essenciais estão instalados.
- `frontend/.env.example` — exemplo de configuração para o frontend.

---

## ✅ Próximos passos (opções)
- Adicionar Docker + docker-compose (execução em qualquer OS) 🐳
- Adicionar testes automatizados (pytest) ✅
- Configurar CI/CD (GitHub Actions) 🔁

---

## 🧪 Testes

### Backend
- Implementado com `pytest` + `TestClient` (FastAPI). Rode em `backend/` com:

```powershell
pip install -r backend/requirements.txt
python -m pytest -q
```

**Testes implementados**:
- `test_create_and_get_product` — cria e recupera produto; valida campos e `GET /products/{id}`.
- `test_update_and_delete_product` — atualiza produto com `PUT` e verifica `DELETE` remove o registro.
- `test_list_products` — valida `GET /products`.
- `test_get_product_not_found` — checa 404 para produto inexistente.
- `test_create_movement_entrada_increases_quantity` — movimento `entrada` aumenta quantidade.
- `test_create_movement_saida_decreases_quantity` — movimento `saida` diminui quantidade.
- `test_create_movement_cannot_remove_more_than_available` — garante erro ao retirar mais que disponível.
- `test_create_movement_invalid_type_or_product` — valida tipos inválidos e produto inexistente.
- `test_list_movements` — valida `GET /movements` retorna movimentos.

---

## 🔁 Integração Contínua (GitHub Actions)

Criei um workflow para CI em `.github/workflows/ci.yml` que:

- Executa os testes do backend (`pytest`) em Python 3.11.
- Faz build do frontend (Node 18) para validar que o frontend compila sem erros.

A pipeline é disparada em `push` e `pull_request` nas branches `main`/`master`. Se quiser, posso ajustar a workflow para rodar checks adicionais (linters, coverage, etc.).

