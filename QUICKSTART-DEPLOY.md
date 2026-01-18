# 🚀 Guia Rápido: Deploy com Ngrok

**Tempo estimado:** 5 minutos

## Passo a Passo Simplificado

### 1️⃣ Instalar Ngrok (primeira vez)

```powershell
winget install ngrok
```

Ou baixe de: https://ngrok.com/download

### 2️⃣ Configurar Ngrok (primeira vez)

1. Crie conta: https://dashboard.ngrok.com/signup
2. Copie authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
3. Execute:

```powershell
ngrok config add-authtoken SEU_TOKEN_AQUI
```

### 3️⃣ Executar Script

```powershell
# Na raiz do projeto
.\deploy-ngrok.ps1
```

Aguarde mensagem: `✅ Deploy concluído!`

### 4️⃣ Abrir Túnel

**Em OUTRO terminal:**

```powershell
ngrok http 80
```

### 5️⃣ Copiar URL e Acessar! 🎉

Exemplo de URL que vai aparecer:
```
https://abc123.ngrok-free.app
```

Copie e cole no navegador. Compartilhe com qualquer pessoa!

---

## ❓ Problemas?

### Ngrok pede para criar conta
- Normal no plano gratuito
- Clique em "Visit Site" para continuar

### CORS Error
```powershell
$env:ALLOW_ALL_ORIGINS="true"
docker-compose restart backend
```

### Containers não iniciam
```powershell
docker-compose down -v
docker-compose up -d
```

---

## 📖 Documentação Completa

Para mais detalhes: [DEPLOY.md](DEPLOY.md)

---

**Desenvolvido com ❤️**
