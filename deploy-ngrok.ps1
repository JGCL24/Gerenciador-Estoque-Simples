# deploy-ngrok.ps1
# Script para deploy rápido com ngrok

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🚀 Deploy Gerenciador de Estoque" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Configurar CORS para aceitar qualquer origem
Write-Host "📝 Configurando CORS..." -ForegroundColor Yellow
$env:ALLOW_ALL_ORIGINS="true"
Write-Host "   ✅ CORS configurado para aceitar todas as origens" -ForegroundColor Green
Write-Host ""

# 2. Parar containers antigos (se houver)
Write-Host "🛑 Parando containers antigos..." -ForegroundColor Yellow
docker-compose down 2>$null
Write-Host "   ✅ Containers parados" -ForegroundColor Green
Write-Host ""

# 3. Iniciar Docker Compose
Write-Host "📦 Iniciando containers..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Containers iniciados com sucesso" -ForegroundColor Green
} else {
    Write-Host "   ❌ Erro ao iniciar containers" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 4. Aguardar containers iniciarem
Write-Host "⏳ Aguardando aplicação iniciar (30 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30
Write-Host "   ✅ Aplicação deve estar pronta" -ForegroundColor Green
Write-Host ""

# 5. Verificar status dos containers
Write-Host "🔍 Status dos containers:" -ForegroundColor Cyan
docker-compose ps
Write-Host ""

# 6. Instruções para ngrok
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🌐 Próximos Passos:" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Abra OUTRO terminal PowerShell" -ForegroundColor Yellow
Write-Host "2. Execute: " -ForegroundColor Yellow -NoNewline
Write-Host "ngrok http 80" -ForegroundColor White -BackgroundColor Blue
Write-Host "3. Copie a URL que aparecer (ex: https://abc123.ngrok-free.app)" -ForegroundColor Yellow
Write-Host "4. Acesse a URL no navegador!" -ForegroundColor Yellow
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "📊 URLs Locais (para testar):" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Frontend:  http://localhost" -ForegroundColor White
Write-Host "API:       http://localhost:8000" -ForegroundColor White
Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "✅ Deploy concluído! Aguardando ngrok..." -ForegroundColor Green
Write-Host ""
