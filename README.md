
# Arena Pinheiro - Backend

Sistema de gerenciamento para Arena Pinheiro, desenvolvido em Python com FastAPI e PostgreSQL. O sistema gerencia campos, reservas, comandas, produtos, estoque, compras, pagamentos e usuários.
Todas as tabelas possuem IDs automáticos (SERIAL) como chave primária. Os campos string são validados para evitar SQL injection.

---

## Índice
- Tecnologias Utilizadas
- Pré-requisitos
- Instalação
- Configuração
- Como Executar
- Estrutura do Projeto
- Documentação da API
- Funcionalidades
- Solução de Problemas

---





# ⚽ Arena Pinheiro - Backend

Sistema web para gerenciar campos, reservas, comandas, produtos, estoque, compras, pagamentos e usuários da Arena Pinheiro.

## 📝 Descrição
API desenvolvida em Python com FastAPI e PostgreSQL. Permite o cadastro, consulta, atualização e remoção de todas as entidades do sistema. IDs são automáticos, senhas são salvas com hash seguro e campos string são validados para evitar SQL injection.

## ✨ Funcionalidades
- CRUD completo para campos, reservas, comandas, produtos, estoque, compras, pagamentos e usuários
- IDs automáticos (não precisa informar ao cadastrar)
- Senhas de usuários com hash seguro (bcrypt)
- Validação de campos string para evitar SQL injection
- Documentação automática (Swagger/OpenAPI)
- CORS configurado


## ⚙️ Pré-requisitos e Dependências

<img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" />
<img src="https://img.shields.io/badge/PostgreSQL-12%2B-blue?logo=postgresql" />

- Python 3.8+
- PostgreSQL 12+
- FastAPI 🏎️
- Uvicorn 🚦
- psycopg2-binary 🐘
- Pydantic 🛡️
- bcrypt 🔒
- python-dotenv 🌱

Instale todas as dependências com:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r backend/requirements.txt
pip install python-dotenv
```

## 🗄️ Configuração do Banco de Dados
1. Crie o banco:
   ```sql
   CREATE DATABASE arena_pinheiro;
   ```
2. Importe as tabelas:
   ```bash
   psql -U postgres -d arena_pinheiro -f backend/Arena_Pinheiro.sql
   ```

## ⚙️ Configuração do Ambiente
Crie um arquivo `.env` na raiz do projeto com:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=arena_pinheiro
DB_USER=postgres
DB_PASSWORD=sua_senha
API_HOST=0.0.0.0
API_PORT=8000
```


## ▶️ Como Executar

Execute o backend com:
```bash
python backend/run.py
```
A API estará disponível em http://localhost:8000

## 📚 Documentação
Acesse a documentação interativa em:
- http://localhost:8000/docs

## 📁 Estrutura do Projeto
```
Arena-Pinheiro/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── run.py
│   ├── Arena_Pinheiro.sql
│   ├── requirements.txt
│   ├── routers/
│   └── schemas/
├── .env
├── README.md
```

## 💡 Dicas e Observações
- Não informe IDs ao cadastrar entidades (o banco gera automaticamente)
- Se der erro de conexão, confira o `.env` e se o PostgreSQL está rodando
- Campos nome e senha de usuário aceitam até 255 caracteres
- Para dúvidas, acesse a documentação em `/docs`

---

Desenvolvido com FastAPI, PostgreSQL e Python 3.8+.

│   ├── database.py
