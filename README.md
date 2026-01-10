# 🏟️ Arena Pinheiro - Sistema de Gestão

Sistema completo de gerenciamento para Arena Pinheiro, desenvolvido com FastAPI (backend) e HTML/CSS/JavaScript (frontend). O sistema gerencia campos, reservas, comandas, produtos, estoque, compras, pagamentos e muito mais.

## 📋 Índice

- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação da API](#-documentação-da-api)
- [Funcionalidades](#-funcionalidades)
- [Solução de Problemas](#-solução-de-problemas)

---

## 🛠️ Tecnologias Utilizadas

### Backend

- **FastAPI** (v0.104.1) - Framework web moderno e rápido para construção de APIs REST em Python
  - Alta performance
  - Validação automática de dados com Pydantic
  - Documentação automática (Swagger/OpenAPI)
  - Suporte nativo a async/await

- **Uvicorn** (v0.24.0) - Servidor ASGI de alta performance
  - Suporte a WebSockets
  - Reload automático em desenvolvimento
  - Processamento assíncrono

- **PostgreSQL** - Banco de dados relacional
  - Robustez e confiabilidade
  - Suporte a transações ACID
  - Queries SQL diretas (sem ORM)

- **psycopg2-binary** (v2.9.9) - Adaptador PostgreSQL para Python
  - Conexões eficientes com o banco
  - Suporte a transações

- **Pydantic** (v2.5.0) - Validação de dados usando type hints
  - Validação automática de tipos
  - Schemas para request/response
  - Serialização JSON automática

- **Python 3.8+** - Linguagem de programação
  - Type hints
  - Async/await para operações assíncronas

### Frontend

- **HTML5** - Estrutura semântica da aplicação web
- **CSS3** - Estilização moderna com gradientes e flexbox
- **JavaScript (ES6+)** - Lógica da aplicação
  - Fetch API para requisições HTTP
  - Módulos ES6 para organização
  - Manipulação do DOM
  - Async/await para requisições assíncronas

### Ferramentas de Desenvolvimento

- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **passlib[bcrypt]** - Hash de senhas (preparado para produção)
- **python-jose** - JWT tokens (preparado para autenticação)

---

## 📦 Pré-requisitos

### 1. Python 3.8 ou Superior

**Windows:**
- Baixe em: https://www.python.org/downloads/
- Durante a instalação, marque "Add Python to PATH"
- Verifique a instalação:
```bash
python --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

**macOS:**
```bash
brew install python3
python3 --version
```

### 2. PostgreSQL 12 ou Superior

**Windows:**
- Baixe em: https://www.postgresql.org/download/windows/
- Durante a instalação, defina uma senha para o usuário `postgres`
- O serviço será iniciado automaticamente

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Verificar instalação:**
```bash
psql --version
```

### 3. pip (Gerenciador de Pacotes Python)

Geralmente vem instalado com Python. Verifique:
```bash
pip --version
# ou
pip3 --version
```

Se não estiver instalado:
```bash
python -m ensurepip --upgrade
```

### 4. Navegador Web Moderno

- Google Chrome (recomendado)
- Mozilla Firefox
- Microsoft Edge
- Safari

---

## 🚀 Instalação

### Passo 1: Clonar/Obter o Projeto

```bash
# Se estiver usando Git
git clone <url-do-repositorio>
cd Pinheiro-Arena

# Ou extraia o arquivo ZIP na pasta desejada
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Você verá `(venv)` no início do prompt quando estiver ativo.

### Passo 3: Instalar Dependências do Backend

```bash
pip install -r backend/requirements.txt
```

Isso instalará todas as dependências necessárias:
- FastAPI
- Uvicorn
- psycopg2-binary
- Pydantic
- E outras...

### Passo 4: Configurar Banco de Dados PostgreSQL

#### 4.1. Criar o Banco de Dados

Abra o terminal e conecte-se ao PostgreSQL:

**Windows (PSQL):**
```bash
psql -U postgres
```

**Linux/macOS:**
```bash
sudo -u postgres psql
```

Execute os seguintes comandos SQL:
```sql
CREATE DATABASE arena_pinheiro;
\q
```

#### 4.2. Criar as Tabelas

Execute o script SQL fornecido:

**Windows:**
```bash
psql -U postgres -d arena_pinheiro -f backend\Arena_Pinheiro.sql
```

**Linux/macOS:**
```bash
psql -U postgres -d arena_pinheiro -f backend/Arena_Pinheiro.sql
```

Você será solicitado a inserir a senha do PostgreSQL. Se tudo estiver correto, verá a mensagem `BEGIN` e `END` indicando que o script foi executado.

---

## ⚙️ Configuração

### Configurar Variáveis de Ambiente

Crie um arquivo `.env` na **raiz do projeto** com o seguinte conteúdo:

```env
# Configuração do Banco de Dados PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=arena_pinheiro
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

**Importante:**
- Substitua `sua_senha_aqui` pela senha do seu PostgreSQL
- Se o PostgreSQL estiver em outro servidor, altere `DB_HOST`
- Se usar outra porta, altere `DB_PORT`
- Se criar outro usuário, altere `DB_USER`

**Exemplo de .env:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=arena_pinheiro
DB_USER=postgres
DB_PASSWORD=minhasenha123
```

---

## 🎯 Como Executar

### Executando o Backend (API)

#### Opção 1: Usando uvicorn diretamente (Recomendado)

Da **raiz do projeto**:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Parâmetros explicados:**
- `--reload`: Recarrega automaticamente quando há mudanças no código
- `--host 0.0.0.0`: Permite acesso de qualquer IP (importante para desenvolvimento)
- `--port 8000`: Porta onde a API ficará disponível

#### Opção 2: Usando o script run.py como módulo

Da **raiz do projeto**:
```bash
python -m backend.run
```

#### Opção 3: Executando de dentro da pasta backend

```bash
cd backend
python run.py
```

#### Verificar se está funcionando

Após executar qualquer um dos comandos acima, você verá algo como:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Conexão com banco de dados estabelecida!
INFO:     Application startup complete.
```

**Testar a API:**

1. Abra o navegador e acesse: http://localhost:8000
   - Deve mostrar: `{"message":"API Arena Pinheiro","version":"1.0.0","docs":"/docs"}`

2. Acesse a documentação interativa: http://localhost:8000/docs
   - Interface Swagger para testar os endpoints

3. Verifique a saúde da API: http://localhost:8000/health
   - Deve mostrar: `{"status":"healthy","database":"connected"}`

### Executando o Frontend

#### Opção 1: Servidor HTTP Python (Recomendado)

**Terminal 1 - Backend (já deve estar rodando):**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**

Da **raiz do projeto**:
```bash
cd frontend
python -m http.server 8080
```

Ou da pasta frontend:
```bash
# Windows
cd frontend
python -m http.server 8080

# Linux/macOS
cd frontend
python3 -m http.server 8080
```

Acesse: **http://localhost:8080/frontend.html**

#### Opção 2: Abrir diretamente no navegador

**Nota:** Algumas funcionalidades podem não funcionar devido a políticas CORS.

1. Abra o arquivo `frontend/frontend.html` diretamente no navegador
2. Na seção "Configuração da API", configure: `http://localhost:8000`
3. Clique em "Testar Conexão"
4. Se aparecer "✓ Conectado", está tudo funcionando!

#### Opção 3: Usando Live Server (VS Code)

Se usar VS Code:
1. Instale a extensão "Live Server"
2. Clique com botão direito em `frontend/frontend.html`
3. Selecione "Open with Live Server"

---

## 📁 Estrutura do Projeto

```
Pinheiro-Arena/
│
├── backend/                          # Código do Backend
│   ├── __init__.py
│   ├── main.py                       # Aplicação principal FastAPI
│   ├── config.py                     # Configurações centralizadas
│   ├── database.py                   # Classe de conexão com PostgreSQL
│   ├── run.py                        # Script para executar a API
│   ├── Arena_Pinheiro.sql            # Script SQL para criar o banco
│   ├── requirements.txt              # Dependências Python
│   │
│   ├── routers/                      # Rotas da API (Módulos separados)
│   │   ├── __init__.py
│   │   ├── usuarios.py               # CRUD de Usuários
│   │   ├── clientes.py               # CRUD de Clientes
│   │   ├── campos.py                 # CRUD de Campos
│   │   ├── reservas.py               # CRUD de Reservas
│   │   ├── produtos.py               # CRUD de Produtos
│   │   ├── estoque.py                # CRUD de Estoque e Movimentações
│   │   ├── mesas.py                  # CRUD de Mesas
│   │   ├── comandas.py               # CRUD de Comandas e Itens
│   │   ├── compras.py                # CRUD de Compras e Itens
│   │   └── pagamentos.py             # CRUD de Pagamentos
│   │
│   └── schemas/                      # Modelos Pydantic (Módulos separados)
│       ├── __init__.py
│       ├── usuarios.py
│       ├── clientes.py
│       ├── campos.py
│       ├── reservas.py
│       ├── produtos.py
│       ├── estoque.py
│       ├── mesas.py
│       ├── comandas.py
│       ├── compras.py
│       └── pagamentos.py
│
├── frontend/                         # Código do Frontend
│   ├── frontend.html                 # Interface web completa (HTML inline)
│   ├── css/
│   │   └── styles.css                # Estilos CSS (preparado para uso futuro)
│   └── js/
│       ├── api.js                    # Configuração e utilitários da API
│       └── utils.js                  # Funções utilitárias (UI, mensagens)
│
├── .env                              # Variáveis de ambiente (criar este arquivo)
├── .gitignore                        # Arquivos ignorados pelo Git
└── README.md                         # Este arquivo
```

---

## 📚 Documentação da API

Quando o backend estiver rodando, acesse:

- **Swagger UI (Interativo):** http://localhost:8000/docs
  - Interface visual para testar todos os endpoints
  - Pode fazer requisições diretamente pelo navegador

- **ReDoc (Documentação):** http://localhost:8000/redoc
  - Documentação formatada e legível

### Principais Endpoints

#### Autenticação e Usuários
- `POST /api/usuarios/` - Criar usuário
- `POST /api/usuarios/login` - Fazer login
- `GET /api/usuarios/` - Listar todos os usuários
- `GET /api/usuarios/{id}` - Obter usuário por ID
- `PUT /api/usuarios/{id}` - Atualizar usuário
- `DELETE /api/usuarios/{id}` - Deletar usuário

#### Gerenciamento de Dados
- **Clientes:** `/api/clientes/` (CRUD completo)
- **Campos:** `/api/campos/` (CRUD completo)
- **Reservas:** `/api/reservas/` (CRUD + listar por cliente)
- **Produtos:** `/api/produtos/` (CRUD completo)
- **Estoque:** `/api/estoque/` (CRUD + movimentações)
- **Mesas:** `/api/mesas/` (CRUD completo)
- **Comandas:** `/api/comandas/` (CRUD + itens)
- **Compras:** `/api/compras/` (CRUD + itens)
- **Pagamentos:** `/api/pagamentos/` (CRUD + vínculos)

---

## ✨ Funcionalidades

### Backend (API REST)

✅ **CRUD Completo** para todas as entidades
✅ **Validação automática** de dados com Pydantic
✅ **Documentação automática** (Swagger/OpenAPI)
✅ **CORS configurado** para permitir requisições do frontend
✅ **Validação de foreign keys** antes de inserções
✅ **Geração automática de IDs** sequenciais
✅ **Mapeamento automático** PascalCase ↔ snake_case
✅ **Tratamento de erros** padronizado
✅ **Health check** endpoint para monitoramento

### Frontend (Interface Web)

✅ **Interface moderna e responsiva**
✅ **Gerenciamento completo de:**
  - Usuários (criação, edição, exclusão, login)
  - Clientes (cadastro e gerenciamento)
  - Campos esportivos (disponibilidade e status)
  - Reservas (agendamento e acompanhamento)
  - Produtos (cadastro com preços e validade)
  - Estoque (controle de quantidade e movimentações)
  - Mesas (status e ocupação)
  - Comandas (itens, valores, status)
  - Compras (registro e histórico)
  - Pagamentos (formas e vínculos)

✅ **Teste de conexão** com a API
✅ **Feedback visual** (mensagens de sucesso/erro)
✅ **Formulários validados** no frontend
✅ **Tabelas dinâmicas** com dados da API

---

## 🐛 Solução de Problemas

### ❌ Erro: "ModuleNotFoundError: No module named 'backend'"

**Causa:** Executando o comando do lugar errado.

**Solução:**
```bash
# Certifique-se de estar na RAIZ do projeto
cd C:\Users\joaog\OneDrive\Documentos\Pinheiro-Arena
python -m backend.run
```

### ❌ Erro: "connection to server at localhost failed"

**Causa:** PostgreSQL não está rodando.

**Solução:**
```bash
# Windows
net start postgresql-x64-XX  # Substitua XX pela versão

# Linux
sudo systemctl start postgresql

# macOS
brew services start postgresql

# Verificar se está rodando
psql -U postgres -c "SELECT version();"
```

### ❌ Erro: "password authentication failed"

**Causa:** Senha incorreta no arquivo `.env`.

**Solução:**
1. Verifique a senha do PostgreSQL
2. Teste a conexão manualmente:
```bash
psql -U postgres -d arena_pinheiro
```
3. Atualize o arquivo `.env` com a senha correta

### ❌ Erro: "database 'arena_pinheiro' does not exist"

**Causa:** Banco de dados não foi criado.

**Solução:**
```sql
-- Conecte-se ao PostgreSQL
psql -U postgres

-- Execute:
CREATE DATABASE arena_pinheiro;
\q

-- Depois execute o script SQL
psql -U postgres -d arena_pinheiro -f backend/Arena_Pinheiro.sql
```

### ❌ Erro: "relation 'Usuario' does not exist"

**Causa:** Tabelas não foram criadas.

**Solução:**
```bash
# Execute novamente o script SQL
psql -U postgres -d arena_pinheiro -f backend/Arena_Pinheiro.sql
```

### ❌ Frontend não consegue conectar à API

**Causa:** CORS ou API não está rodando.

**Solução:**
1. Verifique se o backend está rodando: http://localhost:8000/health
2. Verifique a URL no frontend (deve ser: `http://localhost:8000`)
3. Use um servidor HTTP para o frontend (não abra o arquivo diretamente)
4. Verifique o console do navegador (F12) para erros de CORS

### ❌ Erro: "pip: command not found"

**Causa:** pip não está instalado ou não está no PATH.

**Solução:**
```bash
# Windows
python -m ensurepip --upgrade

# Linux
sudo apt install python3-pip

# macOS
python3 -m ensurepip --upgrade
```

### ❌ Porta 8000 já está em uso

**Causa:** Outra aplicação está usando a porta 8000.

**Solução:**
```bash
# Mude a porta no comando:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001

# E atualize a URL no frontend para: http://localhost:8001
```

---

## 📝 Notas Importantes

### Segurança
⚠️ Esta é uma implementação básica para desenvolvimento. Para produção:
- Implemente autenticação JWT completa
- Use bcrypt para hash de senhas
- Adicione validação de permissões por tipo de usuário
- Implemente rate limiting
- Use HTTPS
- Adicione logs de auditoria
- Implemente validação de entrada mais robusta

### Banco de Dados
- Os nomes das colunas no banco estão em **PascalCase** (ex: `Id_Usuario`)
- Os schemas Pydantic usam **snake_case** (ex: `id_usuario`)
- O mapeamento automático é feito na classe `Database`
- IDs são gerados automaticamente usando `MAX()+1`

### Desenvolvimento
- Use o modo `--reload` apenas em desenvolvimento
- Não commite o arquivo `.env` (já está no .gitignore)
- Mantenha as dependências atualizadas: `pip list --outdated`

---

## 🎓 Comandos Rápidos

```bash
# Instalar dependências
pip install -r backend/requirements.txt

# Executar backend (da raiz)
uvicorn backend.main:app --reload

# Executar frontend (da pasta frontend)
cd frontend
python -m http.server 8080

# Criar banco de dados
psql -U postgres
CREATE DATABASE arena_pinheiro;

# Criar tabelas
psql -U postgres -d arena_pinheiro -f backend/Arena_Pinheiro.sql

# Verificar conexão com banco
psql -U postgres -d arena_pinheiro -c "SELECT COUNT(*) FROM Usuario;"
```

---

## 📄 Licença

Este projeto foi desenvolvido para a Arena Pinheiro.

---

## 👨‍💻 Desenvolvido com

- **FastAPI** - Framework web moderno
- **PostgreSQL** - Banco de dados relacional
- **Python 3.8+** - Linguagem backend
- **HTML5/CSS3/JavaScript** - Frontend web
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

---

**Para mais informações ou dúvidas, consulte a documentação interativa em http://localhost:8000/docs quando a API estiver rodando.**
