# 🧾 Gerenciador de Estoque

Um sistema completo de gestão de estoque com **backend robusto em FastAPI** e **interface moderna em React + Vite**.

**Tech Stack:** FastAPI + SQLModel + SQLite | React 18 + Vite | Docker | GitHub Actions CI/CD

---

## 📋 Índice

1. [Visão Geral](#-visão-geral)
2. [Principais Recursos](#-principais-recursos)
3. [Início Rápido](#-início-rápido)
4. [Arquitetura do Projeto](#-arquitetura-do-projeto)
5. [Pré-requisitos](#-pré-requisitos)
6. [Instalação e Setup](#-instalação-e-setup)
7. [Como Executar](#-como-executar)
8. [Endpoints da API](#-endpoints-da-api)
9. [Componentes Frontend](#-componentes-frontend)
10. [Testes Automatizados](#-testes-automatizados)
11. [Containerização e Docker](#-containerização-e-docker)
12. [Pipeline CI/CD](#-pipeline-cicd)
13. [Deploy e Acesso Público](#-deploy-e-acesso-público)
14. [Troubleshooting](#-troubleshooting)

---

## 🎯 Visão Geral

**Gerenciador de Estoque** é uma solução **full-stack completa** para gerenciar inventário de produtos com rastreamento detalhado de movimentações (entradas, saídas e vendas). O projeto foi desenvolvido seguindo boas práticas de engenharia de software, incluindo arquitetura limpa, testes automatizados, CI/CD e containerização.

### 📦 O Que o Sistema Faz

Este sistema permite que empresas/negócios:
1. **Cadastrem produtos** com informações detalhadas (nome, descrição, preço, quantidade, estoque mínimo)
2. **Registrem movimentações** de entrada (compras, reabastecimento) e saída (vendas, devoluções)
3. **Monitorem estoque** em tempo real com alertas automáticos quando atingir quantidade mínima
4. **Visualizem histórico** completo de todas as movimentações com data/hora e observações
5. **Calculem valor total** do inventário automaticamente

### 🎯 Principais Recursos

- ✅ **CRUD Completo de Produtos** — Criar, ler, atualizar e deletar produtos com validações
- ✅ **Sistema de Movimentações** — Entrada/saída com atualização automática de quantidades
- ✅ **Alertas Inteligentes** — Notificações quando estoque está abaixo do mínimo
- ✅ **Dashboard com Resumo** — Total de produtos, itens em estoque e valor total
- ✅ **Histórico Detalhado** — Rastreamento completo com timestamps e notas
- ✅ **Interface Responsiva** — Funciona perfeitamente em desktop, tablet e mobile
- ✅ **API REST Documentada** — Swagger/OpenAPI para fácil integração
- ✅ **Containerização Docker** — Deploy em qualquer ambiente (Windows, Linux, macOS)
- ✅ **Testes Automatizados** — 9 testes unitários/integração com 100% de cobertura dos endpoints
- ✅ **Pipeline CI/CD** — GitHub Actions com build automático e publicação no Docker Hub
- ✅ **Acesso Público** — Possibilidade de expor na internet com ngrok

### 💡 Tecnologias e Arquitetura

**Backend:**
- **FastAPI** — Framework web moderno e rápido para Python
- **SQLModel** — ORM que combina SQLAlchemy com validação Pydantic
- **PostgreSQL** — Banco de dados relacional (produção)
- **SQLite** — Banco de dados leve (desenvolvimento)
- **Uvicorn** — Servidor ASGI de alta performance

**Frontend:**
- **React 18** — Biblioteca JavaScript para interfaces
- **Vite** — Build tool extremamente rápido
- **Nginx** — Servidor web para servir arquivos estáticos (produção)

**DevOps:**
- **Docker & Docker Compose** — Containerização de toda aplicação
- **GitHub Actions** — Automação de testes e deploy
- **Pytest** — Framework de testes para Python
- **Ngrok** — Túnel para acesso público

### 🏆 Diferenciais do Projeto

1. **Arquitetura Profissional** — Separação clara entre camadas (models, routers, database)
2. **Validações Robustas** — Impede operações inválidas (ex: remover mais itens que disponível)
3. **CORS Configurável** — Suporta desenvolvimento local e deploy público
4. **Migrations Automáticas** — Banco é criado/atualizado automaticamente
5. **Logs Estruturados** — Facilita debugging e monitoramento
6. **Documentação Completa** — README, DEPLOY.md, TESTING.md, CI-CD.md

---

## 🚀 Início Rápido (5 Minutos)

**Quer testar a aplicação em 5 minutos?** Siga estes passos:

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/Gerenciador-Estoque.git
cd Gerenciador-Estoque
```

### 2️⃣ Iniciar com Docker (Recomendado)

```bash
docker-compose up -d
```

### 3️⃣ Aguardar 1 Minuto

```bash
docker-compose ps  # Verificar que todos estão "Up"
```

### 4️⃣ Acessar a Aplicação

Abra no navegador: **http://localhost**

✅ **Pronto!** Aplicação rodando completamente!

---

**Quer mais controle?** Veja a seção [Como Executar](#-como-executar) abaixo.

---

## 🏗️ Arquitetura do Projeto

```
Gerenciador-Estoque/
├── backend/                        # FastAPI REST API
│   ├── app/
│   │   ├── main.py                # Rotas principais (/products, /movements)
│   │   ├── models.py              # Modelos SQLModel (Product, Movement)
│   │   ├── database.py            # Configuração SQLite e sessions
│   │   └── __pycache__/
│   ├── tests/
│   │   ├── conftest.py            # Fixtures pytest
│   │   ├── test_products.py       # Testes CRUD de produtos
│   │   └── test_movements.py      # Testes de movimentações
│   ├── Dockerfile                 # Imagem Docker para backend
│   ├── requirements.txt           # Dependências Python
│   ├── pytest.ini                 # Configuração pytest
│   ├── run.py                     # Script para iniciar servidor
│   └── database.db                # Banco SQLite (gerado automaticamente)
│
├── frontend/                       # React + Vite SPA
│   ├── src/
│   │   ├── api.js                 # Cliente HTTP para API (fetch)
│   │   ├── App.jsx                # Componente raiz (state + lógica)
│   │   ├── main.jsx               # Entrada React
│   │   ├── styles.css             # Estilos globais
│   │   └── components/
│   │       ├── ProductList.jsx    # Grid/tabela de produtos
│   │       ├── ProductCard.jsx    # Card individual de produto
│   │       ├── MovementsCard.jsx  # Últimas movimentações
│   │       ├── Summary.jsx        # Resumo (total, valor)
│   │       ├── Toolbar.jsx        # Barra de ferramentas
│   │       ├── AlertsPanel.jsx    # Alertas de estoque baixo
│   │       ├── ProductForm.jsx    # Formulário CRUD
│   │       ├── MovementForm.jsx   # Formulário movimentações
│   │       ├── SalesForm.jsx      # Formulário de vendas
│   │       └── modals/            # Modal dialogs
│   ├── Dockerfile                 # Imagem Docker para frontend
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf                 # Configuração Nginx
│   └── index.html
│
├── docker-compose.yml             # Orquestração de containers
├── .github/workflows/
│   └── ci.yml                     # Pipeline CI/CD GitHub Actions
├── README.md                      # Este arquivo
├── PROJECT-OVERVIEW.md
├── TESTING.md
├── CI-CD.md
└── .gitignore
```

---

## ⚙️ Pré-requisitos

### Para Desenvolvimento Local

- **Python 3.10+** (testado em 3.10 e 3.11)
- **Node.js 16+** (LTS recomendado)
- **Git** (para controle de versão)
- **pip** e **npm** (gerenciadores de pacotes)

### Verificar Instalação

```bash
python --version      # Python 3.10+
node --version        # Node 16+
npm --version
git --version
```

### Para Docker

- **Docker** (20.10+)
- **Docker Compose** (2.0+)

---

## 🚀 Instalação e Setup

### 1. Clonar o Repositório

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

# Se houver erro de execução, execute:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

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
```

---

## ▶️ Como Executar

### ⚡ Opção 1: Docker Compose (RECOMENDADO - 1 Comando!)

Esta é a forma **mais rápida e fácil**. Toda a aplicação (banco + backend + frontend) inicia com um único comando.

#### **Pré-requisito**

Verificar se Docker está instalado:

```powershell
docker --version
docker-compose --version
```

Se não tiver, instale: [Docker Desktop](https://www.docker.com/products/docker-desktop)

#### **Passo 1: Ir para a Pasta do Projeto**

```powershell
cd "C:\Users\joaog\OneDrive\Documentos\FACULDADE\GC\Gerenciador-Estoque"
```

#### **Passo 2: Iniciar Containers**

```powershell
docker-compose up -d
```

**O que esse comando faz:**
- Cria rede Docker para os containers se comunicarem
- Inicia PostgreSQL (banco de dados)
- Constrói e inicia Backend (FastAPI)
- Constrói e inicia Frontend (React + Nginx)
- Expõe portas: 80, 8000, 5432

**Saída esperada:**
```
[+] Running 4/4
 ✓ Network gerenciador-estoque_default    Created
 ✓ Container gerenciador-estoque-db-1      Started
 ✓ Container gerenciador-estoque-backend-1 Started
 ✓ Container gerenciador-estoque-frontend-1 Started
```

#### **Passo 3: Aguardar 30-60 Segundos**

Os containers levam um tempo para inicializar completamente.

```powershell
# Acompanhar logs (opcional)
docker-compose logs -f

# Ou verificar status
docker-compose ps
```

Status esperado (todos devem estar **Up**):
```
NAME                           STATUS         PORTS
gerenciador-estoque-backend-1  Up 2 minutes   0.0.0.0:8000->8000/tcp
gerenciador-estoque-db-1       Up 2 minutes   0.0.0.0:5432->5432/tcp
gerenciador-estoque-frontend-1 Up 2 minutes   0.0.0.0:80->80/tcp
```

#### **Passo 4: Acessar a Aplicação! 🎉**

Abra no navegador:

| O quê | URL |
|-------|-----|
| **Frontend** | http://localhost |
| **API** | http://localhost:8000 |
| **Swagger Docs** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |

#### **Pronto!** ✅

A aplicação está **totalmente funcional** com:
- ✅ PostgreSQL rodando
- ✅ Backend conectado ao banco
- ✅ Frontend servindo
- ✅ Dados persistem em volume Docker

#### **Comandos Úteis (Docker)**

```powershell
# Iniciar e já ver os logs
docker-compose up -d && docker-compose logs -f

# Ver logs em tempo real
docker-compose logs -f

# Ver logs apenas do backend
docker-compose logs -f backend

# Ver logs do frontend
docker-compose logs -f frontend

# Ver logs do banco de dados
docker-compose logs -f db

# Verificar status dos containers
docker-compose ps

# Parar containers (dados persistem)
docker-compose stop

# Reiniciar containers
docker-compose restart

# Parar e remover containers (dados persistem)
docker-compose down

# Parar e remover tudo (CUIDADO: banco é deletado!)
docker-compose down -v

# Reconstruir imagens após mudanças no código
docker-compose up -d --build

# Executar comando dentro de um container
docker-compose exec backend python -m pytest -v
docker-compose exec frontend npm run build
```

#### **Fluxo Visual (Docker)**

```
Execução: docker-compose up -d
        ↓
[1] Cria rede Docker (bridge)
        ↓
[2] Inicia PostgreSQL 15
    └─ Aguarda porta 5432 ficar pronta
        ↓
[3] Constrói imagem do Backend (Python 3.10 + FastAPI)
[4] Inicia Backend (Uvicorn)
    └─ Conecta ao banco: postgresql://db:5432/estoque
    └─ Aguarda porta 8000 ficar pronta
        ↓
[5] Constrói imagem do Frontend (Node.js + Vite + Nginx)
[6] Inicia Frontend (Nginx)
    └─ Serve arquivos estáticos em port 80
        ↓
[7] ✅ Aplicação pronta em ~1-2 minutos
        ↓
URLs de acesso:
  • Frontend:     http://localhost
  • Backend API:  http://localhost:8000
  • Swagger:      http://localhost:8000/docs
  • PostgreSQL:   localhost:5432
```

#### **Tabela de Portas**

| Serviço | Porta Local | Porta Container | URL |
|---------|-------------|-----------------|-----|
| PostgreSQL | 5432 | 5432 | localhost:5432 |
| Backend | 8000 | 8000 | http://localhost:8000 |
| Frontend | 80 | 80 | http://localhost |

#### **Ciclo de Vida dos Containers**

```
┌─────────────────────────────────────────────┐
│  docker-compose up -d                       │
└──────────────┬──────────────────────────────┘
               ↓
        ✅ RUNNING
               ↓
   ┌───────────┴───────────┐
   ↓                       ↓
docker-compose stop   docker-compose down
   ↓                       ↓
 STOPPED              ❌ REMOVED
   ↓
docker-compose start
   ↓
✅ RUNNING (novamente)
```

#### **Exemplo: Criar Produto via Docker**

Sem sair do PowerShell, você pode fazer requisições:

```powershell
# GET - Listar produtos
Invoke-WebRequest -Uri "http://localhost:8000/products" -Method GET

# POST - Criar produto
$body = @{
    name = "Notebook"
    description = "Laptop profissional"
    price = 2500.00
    quantity = 10
    min_quantity = 2
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/products" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# GET - Acessar Swagger
Start-Process "http://localhost:8000/docs"
```

---

### Opção 2: Execução Local (Desenvolvimento)

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
VITE v5.0.0  ready in 123 ms

➜  Local:   http://localhost:5173/
➜  Press h to show help
```

**Acesse:** [http://localhost:5173/](http://localhost:5173/)

### Opção 2: Docker Compose

```bash
# Na raiz do projeto
docker-compose up -d
```

Acesse:
- **Frontend:** [http://localhost/](http://localhost/)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

Parar containers:
```bash
docker-compose down
```

---

## 📡 Endpoints da API

### Base URL

```
http://localhost:8000
```

### 🛍️ Produtos (`/products`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/products` | Listar todos os produtos |
| `POST` | `/products` | Criar novo produto |
| `GET` | `/products/{id}` | Obter produto específico |
| `PUT` | `/products/{id}` | Atualizar produto |
| `DELETE` | `/products/{id}` | Deletar produto |

#### Schema do Produto

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

#### Exemplos de Uso

**Criar Produto:**

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse Gamer",
    "description": "Mouse RGB com 8000 DPI",
    "price": 199.90,
    "quantity": 10,
    "min_quantity": 2
  }'
```

**Listar Produtos:**

```bash
curl http://localhost:8000/products
```

**Atualizar Produto:**

```bash
curl -X PUT http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 15}'
```

**Deletar Produto:**

```bash
curl -X DELETE http://localhost:8000/products/1
```

---

### 📦 Movimentações (`/movements`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/movements` | Listar movimentações (por data decrescente) |
| `POST` | `/movements` | Registrar entrada ou saída |

#### Schema da Movimentação

```json
{
  "id": 1,
  "product_id": 1,
  "type": "entrada",
  "quantity": 5,
  "note": "Reabastecimento fornecedor",
  "timestamp": "2026-01-17T10:30:00"
}
```

#### Exemplos de Uso

**Registrar Entrada (Reabastecimento):**

```bash
curl -X POST http://localhost:8000/movements \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "type": "entrada",
    "quantity": 10,
    "note": "Reabastecimento - Fornecedor X"
  }'
```

**Registrar Saída (Venda):**

```bash
curl -X POST http://localhost:8000/movements \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "type": "saida",
    "quantity": 2,
    "note": "Venda cliente João"
  }'
```

**Listar Movimentações:**

```bash
curl http://localhost:8000/movements
```

#### Tipos de Movimentação

- **`entrada`** — Aumenta a quantidade em estoque
- **`saida`** — Diminui a quantidade em estoque

---

## 🎨 Componentes Frontend

### Estrutura dos Componentes

```
src/components/
├── ProductList.jsx           # Grid/tabela com todos os produtos
├── ProductCard.jsx           # Card individual de produto
├── ProductForm.jsx           # Formulário criar/editar produto
├── MovementsCard.jsx         # Card com últimas 5 movimentações
├── MovementForm.jsx          # Formulário registrar movimentação
├── SalesForm.jsx             # Formulário rápido de vendas
├── Summary.jsx               # Resumo (total items, valor total)
├── Toolbar.jsx               # Barra superior com filtros/ações
├── AlertsPanel.jsx           # Alertas de estoque baixo
├── Modal.jsx                 # Componente base para modais
├── ModalsContainer.jsx       # Container de múltiplos modais
└── modals/
    ├── ProductModal.jsx      # Modal CRUD de produtos
    ├── MovementModal.jsx     # Modal de movimentações
    ├── MovementDetailsModal.jsx  # Detalhes de movimentação
    ├── QuickAddModal.jsx     # Quick add rápido
    └── SaleModal.jsx         # Modal de vendas rápidas
```

### Componentes Principais

**ProductList** — Exibe todos os produtos em grid/tabela com ações (editar, deletar, movimentar)

**Summary** — Mostra:
- Total de produtos no catálogo
- Total de itens em estoque
- Valor total em estoque

**AlertsPanel** — Lista produtos com estoque abaixo do mínimo, destacando quais precisam de reabastecimento

**MovementsCard** — Histórico das últimas 5 movimentações com tipo, quantidade e timestamp

---

## 🧪 Testes Automatizados

O projeto possui uma **suite completa de testes automatizados** que garantem o funcionamento correto da API e protegem contra regressões. Utilizamos **pytest** com fixtures para criar ambientes de teste isolados.

### 📊 Visão Geral dos Testes

- **Total de Testes:** 9
- **Framework:** pytest + httpx (TestClient)
- **Cobertura:** 100% dos endpoints da API
- **Banco de Dados:** SQLite em memória (testes isolados)
- **Tempo de Execução:** ~0.4 segundos

### 🚀 Como Executar os Testes

```bash
cd backend

# Ativar ambiente virtual
# Windows:
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# Executar todos os testes
python -m pytest -v

# Executar com saída detalhada
python -m pytest -v --tb=short

# Executar apenas testes de produtos
python -m pytest tests/test_products.py -v

# Executar apenas testes de movimentações
python -m pytest tests/test_movements.py -v

# Gerar relatório de cobertura
python -m pytest --cov=app --cov-report=term-missing

# Gerar relatório HTML de cobertura
python -m pytest --cov=app --cov-report=html
```

### 📝 Suite de Testes: Produtos (`test_products.py`)

#### ✅ Teste 1: `test_create_and_get_product`

**O que testa:**
- Criação de um produto via `POST /products`
- Recuperação do produto via `GET /products/{id}`
- Validação de todos os campos retornados

**Cenário:**
```python
# Cria produto
POST /products
{
  "name": "Notebook Dell",
  "description": "Laptop profissional",
  "price": 3500.00,
  "quantity": 10,
  "min_quantity": 2
}

# Verifica criação
GET /products/{id}
Espera: Status 200 + dados corretos
```

**O que valida:**
- ✓ Produto é criado com ID gerado automaticamente
- ✓ Todos os campos são salvos corretamente
- ✓ GET retorna os mesmos dados do POST

---

#### ✅ Teste 2: `test_update_and_delete_product`

**O que testa:**
- Atualização parcial de produto via `PUT /products/{id}`
- Deleção de produto via `DELETE /products/{id}`
- Verificação que produto não existe após deleção

**Cenário:**
```python
# 1. Criar produto
POST /products {...}

# 2. Atualizar apenas quantidade
PUT /products/{id}
{"quantity": 25}

# 3. Verificar atualização
GET /products/{id}
Espera: quantity = 25 (outros campos inalterados)

# 4. Deletar produto
DELETE /products/{id}
Espera: Status 200/204

# 5. Tentar buscar produto deletado
GET /products/{id}
Espera: Status 404
```

**O que valida:**
- ✓ Atualização parcial funciona (não precisa enviar todos os campos)
- ✓ DELETE remove produto do banco
- ✓ Produto deletado retorna 404 ao tentar acessar

---

#### ✅ Teste 3: `test_list_products`

**O que testa:**
- Listagem de múltiplos produtos via `GET /products`
- Garantia que todos os produtos criados aparecem na lista

**Cenário:**
```python
# Criar 3 produtos
POST /products {"name": "Mouse"...}
POST /products {"name": "Teclado"...}
POST /products {"name": "Monitor"...}

# Listar todos
GET /products
Espera: Lista com 3 produtos
```

**O que valida:**
- ✓ Endpoint retorna lista (array)
- ✓ Todos os produtos criados aparecem
- ✓ Cada produto tem todos os campos esperados

---

#### ✅ Teste 4: `test_get_product_not_found`

**O que testa:**
- Tratamento de erro ao buscar produto inexistente

**Cenário:**
```python
GET /products/99999
Espera: Status 404
```

**O que valida:**
- ✓ API retorna 404 para IDs inexistentes
- ✓ Mensagem de erro apropriada
- ✓ Não ocorre erro 500 (crash)

---

### 📝 Suite de Testes: Movimentações (`test_movements.py`)

#### ✅ Teste 5: `test_create_movement_entrada_increases_quantity`

**O que testa:**
- Movimentação de entrada aumenta quantidade do produto

**Cenário:**
```python
# 1. Criar produto com 10 unidades
POST /products {"quantity": 10, ...}

# 2. Registrar entrada de 5 unidades
POST /movements
{
  "product_id": 1,
  "type": "entrada",
  "quantity": 5,
  "note": "Compra fornecedor"
}

# 3. Verificar quantidade atualizada
GET /products/1
Espera: quantity = 15 (10 + 5)
```

**O que valida:**
- ✓ Movimentação é registrada
- ✓ Quantidade do produto aumenta corretamente
- ✓ Histórico de movimentação é salvo

---

#### ✅ Teste 6: `test_create_movement_saida_decreases_quantity`

**O que testa:**
- Movimentação de saída diminui quantidade do produto

**Cenário:**
```python
# 1. Criar produto com 10 unidades
POST /products {"quantity": 10, ...}

# 2. Registrar saída de 3 unidades
POST /movements
{
  "product_id": 1,
  "type": "saida",
  "quantity": 3,
  "note": "Venda cliente"
}

# 3. Verificar quantidade atualizada
GET /products/1
Espera: quantity = 7 (10 - 3)
```

**O que valida:**
- ✓ Movimentação de saída é registrada
- ✓ Quantidade do produto diminui corretamente
- ✓ Timestamp é registrado automaticamente

---

#### ✅ Teste 7: `test_create_movement_cannot_remove_more_than_available`

**O que testa:**
- Validação de negócio: não permitir remover mais itens que existem

**Cenário:**
```python
# 1. Criar produto com 5 unidades
POST /products {"quantity": 5, ...}

# 2. Tentar remover 10 unidades (INVÁLIDO)
POST /movements
{
  "product_id": 1,
  "type": "saida",
  "quantity": 10
}

Espera: Status 400 (Bad Request)
Mensagem: "Quantidade insuficiente em estoque"
```

**O que valida:**
- ✓ Validação de negócio funciona
- ✓ Retorna erro apropriado (400)
- ✓ Quantidade do produto não muda
- ✓ Movimentação inválida não é registrada

---

#### ✅ Teste 8: `test_create_movement_invalid_type_or_product`

**O que testa:**
- Validação de tipo de movimentação inválido
- Validação de produto inexistente

**Cenário 1 - Tipo Inválido:**
```python
POST /movements
{
  "product_id": 1,
  "type": "INVALIDO",  # Deve ser "entrada" ou "saida"
  "quantity": 5
}

Espera: Status 400/422
```

**Cenário 2 - Produto Inexistente:**
```python
POST /movements
{
  "product_id": 99999,  # Não existe
  "type": "entrada",
  "quantity": 5
}

Espera: Status 404
```

**O que valida:**
- ✓ Tipos inválidos são rejeitados
- ✓ Produtos inexistentes retornam 404
- ✓ Validações do Pydantic funcionam

---

#### ✅ Teste 9: `test_list_movements`

**O que testa:**
- Listagem de movimentações em ordem decrescente por data

**Cenário:**
```python
# 1. Criar produto
POST /products {...}

# 2. Criar várias movimentações
POST /movements {"type": "entrada", "quantity": 10}
POST /movements {"type": "saida", "quantity": 3}
POST /movements {"type": "entrada", "quantity": 5}

# 3. Listar movimentações
GET /movements
Espera: Lista com 3 movimentações (mais recente primeiro)
```

**O que valida:**
- ✓ Todas as movimentações são listadas
- ✓ Ordem é decrescente por timestamp
- ✓ Dados completos (product_id, type, quantity, note, timestamp)

---

### 🎯 Fixtures de Teste (`conftest.py`)

O arquivo `conftest.py` contém fixtures reutilizáveis:

```python
@pytest.fixture(name="session")
def session_fixture():
    """Cria banco SQLite em memória para testes isolados"""
    
@pytest.fixture(name="client")
def client_fixture(session):
    """Cria cliente HTTP para testar endpoints"""
```

**Vantagens:**
- ✓ Cada teste tem banco de dados limpo
- ✓ Testes são independentes (não interferem entre si)
- ✓ Execução rápida (banco em memória)
- ✓ Não afeta banco de produção/desenvolvimento

---

### 📊 Saída Esperada dos Testes

```bash
$ python -m pytest -v

==================== test session starts =====================
platform win32 -- Python 3.13.6, pytest-9.0.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\...\backend
configfile: pytest.ini
testpaths: tests
collected 9 items

tests/test_movements.py::test_create_movement_entrada_increases_quantity PASSED [ 11%]
tests/test_movements.py::test_create_movement_saida_decreases_quantity PASSED [ 22%]
tests/test_movements.py::test_create_movement_cannot_remove_more_than_available PASSED [ 33%]
tests/test_movements.py::test_create_movement_invalid_type_or_product PASSED [ 44%]
tests/test_movements.py::test_list_movements PASSED [ 55%]
tests/test_products.py::test_create_and_get_product PASSED [ 66%]
tests/test_products.py::test_update_and_delete_product PASSED [ 77%]
tests/test_products.py::test_list_products PASSED [ 88%]
tests/test_products.py::test_get_product_not_found PASSED [100%]

=============== 9 passed in 0.42s ===============
```

### ✅ Resumo: O Que os Testes Garantem

| Categoria | O que é testado |
|-----------|-----------------|
| **CRUD** | Criar, ler, atualizar, deletar produtos |
| **Validações** | Campos obrigatórios, tipos corretos |
| **Regras de Negócio** | Não remover mais que disponível |
| **Movimentações** | Entrada/saída atualizam quantidades |
| **Erros** | 404 para não encontrado, 400 para dados inválidos |
| **Integridade** | Dados persistem corretamente no banco |
| **Histórico** | Movimentações são registradas com timestamp |

**Cobertura:** 100% dos endpoints da API ✅

---

## 🐳 Containerização e Docker

O projeto é **totalmente containerizado** usando Docker e Docker Compose, permitindo executar toda a aplicação (banco de dados + backend + frontend) com um único comando em qualquer sistema operacional.

### 🎯 Por Que Docker?

- ✅ **Portabilidade** — Roda igual em Windows, macOS, Linux
- ✅ **Isolamento** — Não interfere com outras aplicações
- ✅ **Reprodutibilidade** — Mesmo ambiente em dev/produção
- ✅ **Simplicidade** — Um comando inicia tudo
- ✅ **Escalabilidade** — Fácil adicionar mais containers

### 📦 Arquitetura dos Containers

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Container 1: PostgreSQL 15                      │       │
│  │  ─────────────────────────────────────────────── │       │
│  │  • Image: postgres:15-alpine                     │       │
│  │  • Porta: 5432                                   │       │
│  │  • Volume: db_data (persistência)                │       │
│  │  • Variáveis:                                    │       │
│  │    - POSTGRES_USER=postgres                      │       │
│  │    - POSTGRES_PASSWORD=postgres                  │       │
│  │    - POSTGRES_DB=estoque                         │       │
│  └──────────────────────────────────────────────────┘       │
│                          ↓ conexão TCP                        │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Container 2: Backend (FastAPI)                  │       │
│  │  ─────────────────────────────────────────────── │       │
│  │  • Build: ./backend/Dockerfile                   │       │
│  │  • Porta: 8000 (mapeada para host)               │       │
│  │  • Comando: uvicorn app.main:app                 │       │
│  │  • Variáveis:                                    │       │
│  │    - DATABASE_URL=postgresql://...@db:5432       │       │
│  │    - ALLOW_ALL_ORIGINS (CORS)                    │       │
│  │  • Depends_on: db (inicia após banco)            │       │
│  └──────────────────────────────────────────────────┘       │
│                          ↓ requisições HTTP                   │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Container 3: Frontend (React + Nginx)           │       │
│  │  ─────────────────────────────────────────────── │       │
│  │  • Build: ./frontend/Dockerfile (multi-stage)    │       │
│  │  • Porta: 80 (mapeada para host)                 │       │
│  │  • Stage 1: Node.js (build Vite)                 │       │
│  │  • Stage 2: Nginx (serve arquivos)               │       │
│  │  • Depends_on: backend (inicia após API)         │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 📄 Dockerfile do Backend

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary  # Driver PostgreSQL

# Copiar código da aplicação
COPY . .

# Expor porta da API
EXPOSE 8000

# Comando para iniciar servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**O que faz:**
1. Usa imagem base Python 3.10 slim (menor tamanho)
2. Instala todas as dependências (FastAPI, SQLModel, etc.)
3. Instala driver PostgreSQL
4. Copia código da aplicação
5. Expõe porta 8000
6. Inicia Uvicorn em produção

### 📄 Dockerfile do Frontend (Multi-Stage)

```dockerfile
# frontend/Dockerfile

# Stage 1: Build (Node.js)
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build  # Gera /app/dist

# Stage 2: Serve (Nginx)
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**O que faz:**
1. **Stage 1 (build):** Compila React com Vite
2. **Stage 2 (runtime):** Copia apenas arquivos compilados para Nginx
3. Resultado: Imagem final muito menor (~25MB vs ~500MB)
4. Nginx serve arquivos estáticos otimizados

### 📄 docker-compose.yml

```yaml
services:
  # Banco de Dados
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=estoque
    volumes:
      - db_data:/var/lib/postgresql/data  # Persistência
    ports:
      - "5432:5432"

  # Backend API
  backend:
    build: 
      context: ./backend
    restart: always
    ports:
      - "8000:8000"
    depends_on:
      - db  # Aguarda banco iniciar
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/estoque
      - ALLOW_ALL_ORIGINS=${ALLOW_ALL_ORIGINS:-false}

  # Frontend
  frontend:
    build: 
      context: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend  # Aguarda backend iniciar

# Volumes para persistência
volumes:
  db_data:
```

### 🚀 Como Usar Docker Compose

#### **1. Iniciar Toda a Aplicação**

```bash
# Na raiz do projeto
docker-compose up -d
```

**O que acontece:**
1. ✅ Baixa imagem PostgreSQL (se não tiver)
2. ✅ Constrói imagem do backend (lê Dockerfile)
3. ✅ Constrói imagem do frontend (lê Dockerfile)
4. ✅ Cria rede Docker para containers se comunicarem
5. ✅ Inicia container PostgreSQL
6. ✅ Aguarda banco ficar pronto
7. ✅ Inicia container Backend (conecta ao banco)
8. ✅ Aguarda backend ficar pronto
9. ✅ Inicia container Frontend
10. ✅ Aplicação totalmente funcional em ~1 minuto

**Saída esperada:**
```
[+] Running 4/4
 ✓ Network gerenciador-estoque_default    Created
 ✓ Container gerenciador-estoque-db-1      Started
 ✓ Container gerenciador-estoque-backend-1 Started
 ✓ Container gerenciador-estoque-frontend-1 Started
```

#### **2. Verificar Status**

```bash
docker-compose ps
```

**Saída esperada:**
```
NAME                           SERVICE   STATUS         PORTS
gerenciador-estoque-backend-1  backend   Up 2 minutes   0.0.0.0:8000->8000/tcp
gerenciador-estoque-db-1       db        Up 2 minutes   0.0.0.0:5432->5432/tcp
gerenciador-estoque-frontend-1 frontend  Up 2 minutes   0.0.0.0:80->80/tcp
```

Todos devem estar **Up** (rodando).

#### **3. Ver Logs**

```bash
# Todos os containers
docker-compose logs -f

# Apenas backend
docker-compose logs -f backend

# Apenas frontend
docker-compose logs -f frontend

# Últimas 50 linhas do banco
docker-compose logs --tail=50 db
```

#### **4. Parar Aplicação**

```bash
# Parar containers (dados do banco PERSISTEM)
docker-compose stop

# Parar e REMOVER containers (dados persistem no volume)
docker-compose down

# Parar, remover containers E DELETAR dados do banco
docker-compose down -v  # CUIDADO: Perda de dados!
```

#### **5. Reiniciar Containers**

```bash
# Reiniciar tudo
docker-compose restart

# Reiniciar apenas backend
docker-compose restart backend
```

#### **6. Reconstruir Após Mudanças no Código**

```bash
# Reconstruir imagens e reiniciar
docker-compose up -d --build

# Reconstruir sem usar cache (do zero)
docker-compose build --no-cache
docker-compose up -d
```

### 🔍 Build Manual de Imagens

```bash
# Backend
docker build -t gerenciador-estoque-backend ./backend

# Frontend
docker build -t gerenciador-estoque-frontend ./frontend

# Executar manualmente
docker run -p 8000:8000 gerenciador-estoque-backend
docker run -p 80:80 gerenciador-estoque-frontend
```

### 📊 Vantagens da Containerização Neste Projeto

| Aspecto | Sem Docker | Com Docker |
|---------|------------|------------|
| **Setup Inicial** | 30-60 min (instalar Python, Node, PostgreSQL) | 2 min (apenas Docker) |
| **Portabilidade** | Funciona só no SO de desenvolvimento | Funciona em Windows, Mac, Linux |
| **Dependências** | Conflitos com outras aplicações | Isolado completamente |
| **Banco de Dados** | Instalar e configurar PostgreSQL | Já vem configurado |
| **Deploy** | Configurar servidor manualmente | `docker-compose up` |
| **Limpeza** | Desinstalar tudo manualmente | `docker-compose down -v` |

### 🎯 Acesso aos Containers

```bash
# Entrar no terminal do backend
docker-compose exec backend sh

# Entrar no PostgreSQL
docker-compose exec db psql -U postgres -d estoque

# Ver arquivos do frontend
docker-compose exec frontend ls /usr/share/nginx/html
```

### 💾 Persistência de Dados

**Volume `db_data`:**
- Dados do PostgreSQL são salvos em volume Docker
- Dados **persistem** mesmo após `docker-compose down`
- Apenas são deletados com `docker-compose down -v`

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect gerenciador-estoque_db_data

# Deletar volume (CUIDADO!)
docker volume rm gerenciador-estoque_db_data
```

### 🌐 URLs de Acesso

Após `docker-compose up -d`:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost | Interface React |
| **Backend API** | http://localhost:8000 | Endpoints da API |
| **Swagger Docs** | http://localhost:8000/docs | Documentação interativa |
| **ReDoc** | http://localhost:8000/redoc | Documentação alternativa |
| **PostgreSQL** | localhost:5432 | Conexão direta ao banco |

### ⚙️ Variáveis de Ambiente

Para expor aplicação na internet (ngrok):

```bash
# Windows
$env:ALLOW_ALL_ORIGINS="true"
docker-compose up -d

# Linux/macOS
ALLOW_ALL_ORIGINS=true docker-compose up -d
```

### 🐛 Troubleshooting Docker

**Porta já está em uso:**
```bash
# Mudar porta no docker-compose.yml
ports:
  - "8080:80"  # Frontend agora em localhost:8080
```

**Container não inicia:**
```bash
docker-compose logs backend  # Ver erro
docker-compose down -v       # Limpar tudo
docker-compose up -d         # Reiniciar
```

**Rebuild não funciona:**
```bash
docker-compose build --no-cache
docker-compose up -d
```

### ✅ Resumo: Fluxo Completo

```bash
# 1. Clonar projeto
git clone https://github.com/seu-usuario/Gerenciador-Estoque.git
cd Gerenciador-Estoque

# 2. Iniciar containers
docker-compose up -d

# 3. Aguardar 30-60 segundos

# 4. Acessar
# http://localhost (frontend)
# http://localhost:8000/docs (API)

# 5. Parar quando terminar
docker-compose down
```

**Pronto! Aplicação completa rodando em containers.** 🎉

```bash
# Iniciar todo stack
docker-compose up -d

# Parar containers
docker-compose down

# Ver logs do backend
docker-compose logs -f backend

# Ver logs do frontend
docker-compose logs -f frontend
```

**URLs ao usar Docker Compose:**
- Frontend: [http://localhost/](http://localhost/)
- API: [http://localhost:8000](http://localhost:8000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Dockerfile - Backend

- Image base: `python:3.11-slim`
- Instala dependências via `pip`
- Expõe porta **8000**
- Comando: `python run.py`

### Dockerfile - Frontend

- Build: `node:18-alpine` com Vite
- Runtime: `nginx:alpine` para servir arquivos estáticos
- Nginx proxy para API em `/api`
- Expõe porta **80**

---

## 🔄 Pipeline CI/CD

A pipeline GitHub Actions automatiza testes e build a cada commit/pull request.

### O que faz a Pipeline

```
[Push ou Pull Request]
        ↓
[Backend Tests (Python 3.10 & 3.11)]
        ↓
[Frontend Build (Node.js)]
        ↓
[Summary - Sucesso ✅ ou Falha ❌]
```

### Configuração (`.github/workflows/ci.yml`)

#### 1. Backend Tests (backend-tests)

- Roda em Python **3.10 e 3.11**
- Executa: `python -m pytest -v`
- Cache de dependências pip
- Gera relatório de cobertura

#### 2. Frontend Build (frontend-build)

- Executa após backend passar
- Node.js **18**
- Executa: `npm run build`
- Cache de dependências npm

#### 3. Summary

- Verifica se tudo passou
- Retorna status geral da pipeline

### Triggers

- ✅ Push em `main`, `master`, `develop`
- ✅ Pull Requests em `main`, `master`, `develop`

### Status da Pipeline

Veja o status em: **Actions** → **CI/CD** no repositório GitHub

---

## 🌐 Deploy e Acesso Público

### Método Rápido: Ngrok (Máquina Local)

Para expor sua aplicação na internet em **5 minutos**:

#### 1. Instalar Ngrok

```powershell
# Windows
winget install ngrok

# Ou baixar de: https://ngrok.com/download
```

#### 2. Configurar (primeira vez apenas)

```powershell
# Criar conta gratuita em https://dashboard.ngrok.com/signup
# Copiar authtoken e executar:
ngrok config add-authtoken SEU_TOKEN_AQUI
```

#### 3. Executar Script Automatizado

```powershell
# Na raiz do projeto, execute:
.\deploy-ngrok.ps1
```

Isso irá:
- ✅ Configurar CORS para aceitar acesso público
- ✅ Iniciar todos os containers Docker
- ✅ Preparar aplicação para ngrok

#### 4. Abrir Túnel Ngrok

**Em outro terminal:**

```powershell
ngrok http 80
```

#### 5. Acessar pela Internet! 🎉

Copie a URL que aparecer (ex: `https://abc123.ngrok-free.app`) e compartilhe!

**Qualquer pessoa pode acessar de qualquer lugar do mundo.**

### Documentação Completa

Para deploy em servidor VPS, configuração SSL, e mais detalhes:

📖 **[Guia Completo de Deploy (DEPLOY.md)](DEPLOY.md)**

Inclui:
- Deploy com ngrok (detalhado)
- Deploy em servidor VPS (Ubuntu)
- Configuração de SSL/HTTPS
- Troubleshooting completo

---

## 🔧 Variáveis de Ambiente

### Backend (`backend/.env`)

```
# CORS - Permitir acesso de qualquer origem (para ngrok/deploy)
ALLOW_ALL_ORIGINS=true

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
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🆘 Troubleshooting

### Backend não inicia ou erro ao conectar banco

```bash
cd backend

# Deletar banco SQLite corrompido (dados serão perdidos)
rm database.db

# Reiniciar backend
python run.py
```

### Porta 8000 já está em uso

```bash
# Mudar porta
$env:PORT=8001  # Windows
PORT=8001       # macOS/Linux
python run.py
```

### Node modules corrompido ou dependências com erro

```bash
cd frontend

# Limpar cache
rm -r node_modules package-lock.json

# Reinstalar
npm install

# Tentar build novamente
npm run build
```

### Testes falhando com erro de dependências

```bash
cd backend

# Ativar ambiente virtual
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Executar testes
python -m pytest -v
```

### CORS Error ao acessar via ngrok

```bash
# Definir variável de ambiente
$env:ALLOW_ALL_ORIGINS="true"  # Windows
export ALLOW_ALL_ORIGINS=true  # Linux/macOS

# Reiniciar containers
docker-compose restart backend
```

### Erro de CORS ao conectar frontend com backend

Verifique se o frontend está acessando a URL correta:
- URL esperada: `http://localhost:8000`
- Configurar em `frontend/.env`: `VITE_API_URL=http://localhost:8000`

### Docker Compose não inicia

```bash
# Verificar logs
docker-compose logs -f

# Remover containers e volumes antigos
docker-compose down -v

# Reiniciar
docker-compose up -d
```

---

## 📚 Documentação Adicional

- [PROJECT-OVERVIEW.md](PROJECT-OVERVIEW.md) — Visão geral técnica completa
- [TESTING.md](TESTING.md) — Guia completo de testes
- [CI-CD.md](CI-CD.md) — Guia da pipeline GitHub Actions
- [DEPLOY.md](DEPLOY.md) — Guia completo de deploy e acesso público

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

## 📊 Status do Projeto

- ✅ Backend (FastAPI) — Completo
- ✅ Frontend (React + Vite) — Completo
- ✅ Testes Automatizados — Completo (9 testes)
- ✅ Docker & Docker Compose — Completo
- ✅ Pipeline CI/CD (GitHub Actions) — Completo
- ✅ Deploy e Acesso Público (Ngrok) — Completo

---

## 📞 Suporte

Para dúvidas, bugs ou sugestões, abra uma **Issue** no GitHub.

**Última atualização:** 18 de Janeiro de 2026

---

**Desenvolvido com ❤️ para gerenciamento eficiente de estoques.**
