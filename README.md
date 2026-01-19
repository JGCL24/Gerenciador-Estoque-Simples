# 🧾 Gerenciador de Estoque

![CI Status](https://img.shields.io/github/actions/workflow/status/seu-usuario/Gerenciador-Estoque/ci.yml?label=CI&style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=flat-square&logo=vite)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)

Um sistema completo de gestão de estoque com **backend robusto em FastAPI** e **interface moderna em React + Vite**.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Início Rápido](#-início-rápido)
- [Instalação e Execução](#-instalação-e-execução)
- [API Endpoints](#-api-endpoints)
- [Testes](#-testes)
- [Deploy](#-deploy)

---

## 🎯 Visão Geral

**Gerenciador de Estoque** é uma solução **full-stack** para controle de inventário, projetada com foco em performance, escalabilidade e boas práticas de engenharia de software. O sistema permite o rastreamento detalhado de produtos, movimentações de entrada/saída e monitoramento de níveis de estoque em tempo real.

### 🖼️ Preview

*(Adicione screenshots da sua aplicação aqui)*

---

## ✨ Funcionalidades

| Módulo | Recursos |
|--------|----------|
| **📦 Gestão de Produtos** | CRUD completo, controle de quantidade mínima, preços e descrições detalhadas. |
| **🔄 Movimentações** | Registro de entradas (compras) e saídas (vendas) com histórico e notas. |
| **🚨 Alertas Inteligentes** | Notificações visuais quando o estoque atinge o nível mínimo. |
| **📊 Dashboard** | Visão geral com total de itens, valor do inventário e status do sistema. |
| **🛡️ Segurança & Validação** | Proteção contra dados inconsistentes e validações de regras de negócio. |

---

## 🛠 Tecnologias

<div align="center">

| **Backend** | **Frontend** | **DevOps & Infra** |
|:-----------:|:------------:|:------------------:|
| ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) | ![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black) | ![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?logo=docker&logoColor=white) |
| ![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi&logoColor=white) | ![Vite](https://img.shields.io/badge/Vite-Build_Tool-646CFF?logo=vite&logoColor=white) | ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?logo=github-actions&logoColor=white) |
| ![SQLModel](https://img.shields.io/badge/SQLModel-ORM-000000?logo=python&logoColor=white) | ![Tailwind](https://img.shields.io/badge/CSS-Styles-1572B6?logo=css3&logoColor=white) | ![Nginx](https://img.shields.io/badge/Nginx-Server-009639?logo=nginx&logoColor=white) |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white) | ![Axios](https://img.shields.io/badge/JS-Fecth_API-F7DF1E?logo=javascript&logoColor=black) | ![Ngrok](https://img.shields.io/badge/Ngrok-Tunneling-1F1E38?logo=ngrok&logoColor=white) |

</div>

---

## 🚀 Início Rápido

A maneira mais fácil de rodar o projeto é usando **Docker Compose**.

### Pré-requisitos
- [Docker](https://www.docker.com/products/docker-desktop) instalado e rodando.

### 1️⃣ Rodar com um comando
```bash
docker-compose up -d
```

### 2️⃣ Acessar
- **Web App:** [http://localhost](http://localhost)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

> **Nota:** Na primeira execução, pode levar alguns minutos para baixar as imagens e configurar o banco de dados.

---

## 📦 Instalação e Execução

<details>
<summary><strong>🔧 Execução Local (sem Docker)</strong></summary>

### Pré-requisitos
- Python 3.10+
- Node.js 16+
- PostgreSQL (ou SQLite padrão)

### 1. Backend

```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```
O backend rodará em `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```
O frontend rodará em `http://localhost:5173`.

</details>

<details>
<summary><strong>🐳 Comandos Úteis do Docker</strong></summary>

```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar containers
docker-compose stop

# Parar e remover containers (padrão)
docker-compose down

# Reconstruir imagens (se alterar código/dependências)
docker-compose up -d --build
```
</details>

---

## 📡 API Endpoints

A API é RESTful e totalmente documentada via Swagger/OpenAPI.

### Principais Rotas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/products` | Lista todos os produtos |
| `POST` | `/products` | Cria um novo produto |
| `GET` | `/products/{id}` | Detalhes de um produto |
| `PUT` | `/products/{id}` | Atualiza um produto |
| `DELETE` | `/products/{id}` | Remove um produto |
| `GET` | `/movements` | Histórico de movimentações |
| `POST` | `/movements` | Registra entrada/saída de estoque |

> Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para testar os endpoints interativamente.

---

## 🧪 Testes

O projeto possui **100% de cobertura de testes** nos endpoints principais, garantindo confiabilidade.

### Executar Testes
```bash
# Dentro da pasta /backend
pytest -v

# Com relatório de cobertura
pytest --cov=app --cov-report=term-missing
```

**O que é testado?**
- ✅ Criação, leitura, atualização e remoção de produtos.
- ✅ Lógica de movimentação de estoque (entrada soma, saída subtrai).
- ✅ Validação de estoque negativo (impede vendas sem saldo).
- ✅ Tratamento de erros (404 Not Found, 422 Validation Error).

---

## 🚢 Deploy & CI/CD

### Pipeline GitHub Actions
O projeto conta com uma pipeline configurada em `.github/workflows/ci.yml` que:
1. Roda testes automatizados no Backend (Python).
2. Verifica o build do Frontend (Node.js).
3. Só permite merge se tudo passar.

### Deploy Público (Ngrok)
Para expor seu ambiente local para a internet rapidamente:

1. Instale o [Ngrok](https://ngrok.com/).
2. Execute o script de deploy facilitado:
   ```powershell
   .\deploy-ngrok.ps1
   ```
3. Sua aplicação estará acessível mundialmente via URL segura HTTPS.

---

## 📂 Estrutura do Projeto

```
/
├── backend/            # API FastAPI
│   ├── app/           # Lógica da aplicação (Models, Routes)
│   ├── tests/         # Testes automatizados (Pytest)
│   └── ...
├── frontend/           # Interface React
│   ├── src/           # Componentes, Páginas e Estilos
│   └── ...
├── docker-compose.yml  # Orquestração dos containers
└── README.md           # Documentação
```

---

<div align="center">
  <sub>Desenvolvido para a disciplina de Gerência de Configuração.</sub>
</div>
