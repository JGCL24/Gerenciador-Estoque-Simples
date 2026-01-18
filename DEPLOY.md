# 🌐 Deploy e Acesso Público com Ngrok

Este guia mostra como executar a aplicação em um servidor e acessá-la pela internet usando **ngrok** ou **deploy em servidor real**.

---

## 📋 Índice

1. [Opção 1: Acesso Público com Ngrok (Máquina Local)](#opção-1-acesso-público-com-ngrok)
2. [Opção 2: Deploy em Servidor VPS](#opção-2-deploy-em-servidor-vps)
3. [Configuração de Variáveis de Ambiente](#configuração-de-variáveis-de-ambiente)
4. [Troubleshooting](#troubleshooting)

---

## 🚀 Opção 1: Acesso Público com Ngrok

### O que é Ngrok?

Ngrok cria um **túnel seguro** da internet para sua máquina local, permitindo que qualquer pessoa acesse sua aplicação através de uma URL pública.

```
Internet → ngrok.io → Túnel → Sua Máquina (localhost:80)
```

### Passo a Passo Completo

#### **1. Instalar Ngrok**

**Windows (PowerShell):**
```powershell
# Baixar ngrok
winget install ngrok

# Ou baixar manualmente de: https://ngrok.com/download
```

**macOS:**
```bash
brew install ngrok
```

**Linux:**
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

Verificar instalação:
```bash
ngrok version
```

#### **2. Criar Conta no Ngrok (Gratuito)**

1. Acesse: [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
2. Crie uma conta gratuita
3. Copie seu **authtoken** em: [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)

#### **3. Configurar Authtoken**

```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```

#### **4. Iniciar Aplicação com Docker Compose**

```powershell
# Na raiz do projeto
cd "C:\Users\joaog\OneDrive\Documentos\FACULDADE\GC\Gerenciador-Estoque"

# Definir variável para permitir todas as origens (CORS)
$env:ALLOW_ALL_ORIGINS="true"

# Iniciar containers
docker-compose up -d

# Aguardar 30-60 segundos para tudo iniciar
Start-Sleep -Seconds 30

# Verificar se está rodando
docker-compose ps
```

Saída esperada:
```
NAME                           STATUS
gerenciador-estoque-backend-1  Up 1 minute
gerenciador-estoque-db-1       Up 1 minute  
gerenciador-estoque-frontend-1 Up 1 minute
```

#### **5. Abrir Túnel Ngrok**

**Em outro terminal PowerShell:**

```powershell
# Expor porta 80 (frontend)
ngrok http 80
```

Saída esperada:
```
Session Status                online
Account                       seu_email@email.com
Version                       3.x.x
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:80
```

#### **6. Acessar pela Internet! 🎉**

Copie a URL `https://abc123.ngrok-free.app` e:

- ✅ Abra no navegador (qualquer dispositivo)
- ✅ Compartilhe com amigos
- ✅ Teste em celular/tablet
- ✅ Acesse de qualquer lugar do mundo

**URLs Públicas:**
```
Frontend:  https://abc123.ngrok-free.app
API:       https://abc123.ngrok-free.app:8000 (se expor porta 8000 também)
```

#### **7. (Opcional) Expor Backend Também**

Se quiser acessar a API diretamente:

```powershell
# Em outro terminal
ngrok http 8000
```

Isso criará outra URL para a API: `https://xyz456.ngrok-free.app`

---

### 📊 Script Automatizado (Windows)

Crie um arquivo `deploy-ngrok.ps1`:

```powershell
# deploy-ngrok.ps1
Write-Host "🚀 Iniciando deploy com ngrok..." -ForegroundColor Green

# 1. Configurar CORS
$env:ALLOW_ALL_ORIGINS="true"

# 2. Iniciar Docker Compose
Write-Host "📦 Iniciando containers..." -ForegroundColor Cyan
docker-compose up -d

# 3. Aguardar containers iniciarem
Write-Host "⏳ Aguardando 30 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# 4. Verificar status
Write-Host "🔍 Verificando containers..." -ForegroundColor Cyan
docker-compose ps

# 5. Iniciar ngrok em background
Write-Host ""
Write-Host "🌐 Iniciando ngrok..." -ForegroundColor Green
Write-Host "Execute em outro terminal: ngrok http 80" -ForegroundColor Yellow
Write-Host ""
Write-Host "✅ Aplicação pronta! Aguarde o ngrok iniciar." -ForegroundColor Green
```

Executar:
```powershell
.\deploy-ngrok.ps1
```

---

## 🖥️ Opção 2: Deploy em Servidor VPS

### Pré-requisitos

- Servidor Linux (Ubuntu 22.04 LTS recomendado)
- Docker e Docker Compose instalados
- Acesso SSH ao servidor
- Domínio ou IP público

### Passo a Passo

#### **1. Conectar ao Servidor**

```bash
ssh usuario@seu-servidor.com
```

#### **2. Instalar Docker**

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker --version
docker-compose --version
```

#### **3. Clonar Repositório**

```bash
git clone https://github.com/seu-usuario/Gerenciador-Estoque.git
cd Gerenciador-Estoque
```

#### **4. Configurar Variáveis de Ambiente**

```bash
# Criar arquivo .env
cat > .env << EOF
ALLOW_ALL_ORIGINS=true
DATABASE_URL=postgresql://postgres:postgres@db:5432/estoque
EOF
```

#### **5. Iniciar Aplicação**

```bash
# Iniciar com Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f
```

#### **6. Configurar Firewall**

```bash
# Permitir portas 80 e 443
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

#### **7. (Opcional) Configurar Nginx Reverso + SSL**

```bash
# Instalar Nginx
sudo apt install nginx certbot python3-certbot-nginx -y

# Criar configuração
sudo nano /etc/nginx/sites-available/estoque

# Adicionar:
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Ativar site
sudo ln -s /etc/nginx/sites-available/estoque /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Configurar SSL (HTTPS)
sudo certbot --nginx -d seu-dominio.com
```

#### **8. Acessar**

```
http://seu-dominio.com
https://seu-dominio.com (com SSL)
```

---

## ⚙️ Configuração de Variáveis de Ambiente

### Backend

Criar arquivo `backend/.env`:

```env
# CORS
ALLOW_ALL_ORIGINS=true

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/estoque

# Server
HOST=0.0.0.0
PORT=8000
```

### Frontend

Criar arquivo `frontend/.env`:

```env
# API URL (mudar conforme ambiente)
VITE_API_URL=https://sua-url-ngrok.ngrok-free.app
```

---

## 🐛 Troubleshooting

### Ngrok mostra "Tunnel not found" ou erro 404

```bash
# Verificar se aplicação está rodando
docker-compose ps

# Verificar logs
docker-compose logs frontend

# Reiniciar
docker-compose restart
```

### CORS Error ao acessar pela URL ngrok

```bash
# Verificar variável de ambiente
echo $env:ALLOW_ALL_ORIGINS  # Windows
echo $ALLOW_ALL_ORIGINS      # Linux/macOS

# Deve retornar: true

# Se não, definir:
$env:ALLOW_ALL_ORIGINS="true"  # Windows
export ALLOW_ALL_ORIGINS=true  # Linux/macOS

# Reiniciar backend
docker-compose restart backend
```

### Ngrok pede para criar conta (tela de aviso)

Isso é normal no plano gratuito. Clique em "Visit Site" para continuar.

### Aplicação lenta via ngrok

Normal no plano gratuito. Para melhor performance:
- Use plano pago do ngrok
- Ou faça deploy em servidor real (VPS)

### Backend não conecta ao banco

```bash
# Verificar logs do banco
docker-compose logs db

# Recriar banco
docker-compose down -v
docker-compose up -d
```

---

## 📊 Comparação de Métodos

| Método | Custo | Velocidade | Uptime | Dificuldade |
|--------|-------|------------|--------|-------------|
| **Ngrok (gratuito)** | Grátis | Médio | Temporário | ⭐ Fácil |
| **Ngrok (pago)** | $8-20/mês | Bom | 24/7 | ⭐ Fácil |
| **VPS (DigitalOcean)** | $4-6/mês | Ótimo | 24/7 | ⭐⭐ Médio |
| **AWS/Azure** | Variável | Ótimo | 24/7 | ⭐⭐⭐ Difícil |

---

## 🎯 Recomendações

**Para desenvolvimento/demo:**
- ✅ Use ngrok (rápido e fácil)

**Para produção:**
- ✅ Use VPS (DigitalOcean, Linode, Vultr)
- ✅ Configure SSL (certbot)
- ✅ Configure backup automático
- ✅ Use PostgreSQL gerenciado

---

## 📚 Recursos Adicionais

- [Documentação Ngrok](https://ngrok.com/docs)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
- [Docker Compose em Produção](https://docs.docker.com/compose/production/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**Última atualização:** 18 de Janeiro de 2026

🎉 **Agora sua aplicação está acessível na internet!**
