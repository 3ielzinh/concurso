# Script para popular o banco PostgreSQL do Render
# Execute este script para migrar e popular os dados

Write-Host "🚀 Iniciando migração para PostgreSQL do Render..." -ForegroundColor Cyan
Write-Host ""

# 1. Backup do .env atual
Write-Host "📦 Fazendo backup do .env local..." -ForegroundColor Yellow
Copy-Item .env .env.backup -Force
Write-Host "✅ Backup criado: .env.backup" -ForegroundColor Green
Write-Host ""

# 2. Usar configurações de produção
Write-Host "🔄 Configurando para usar PostgreSQL do Render..." -ForegroundColor Yellow
Copy-Item .env.production .env -Force
Write-Host "✅ Configuração de produção ativada" -ForegroundColor Green
Write-Host ""

# 3. Rodar migrações
Write-Host "📊 Executando migrações no PostgreSQL..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao executar migrações!" -ForegroundColor Red
    Copy-Item .env.backup .env -Force
    exit 1
}
Write-Host "✅ Migrações concluídas" -ForegroundColor Green
Write-Host ""

# 4. Popular dados
Write-Host "🌱 Populando banco de dados..." -ForegroundColor Yellow
Get-Content populate_data.py | python manage.py shell
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Aviso: Pode haver dados duplicados (normal se já rodou antes)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Dados populados com sucesso" -ForegroundColor Green
}
Write-Host ""

# 5. Criar superusuário
Write-Host "👤 Agora vamos criar um superusuário..." -ForegroundColor Yellow
Write-Host "   (Se quiser pular, pressione Ctrl+C)" -ForegroundColor Gray
Write-Host ""
python manage.py createsuperuser
Write-Host ""

# 6. Restaurar .env local
Write-Host "🔙 Restaurando configuração local..." -ForegroundColor Yellow
Copy-Item .env.backup .env -Force
Remove-Item .env.backup -Force
Write-Host "✅ Configuração local restaurada" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 CONCLUÍDO!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Acesse o painel do Render e adicione as variáveis de ambiente:" -ForegroundColor White
Write-Host "      DATABASE_URL=postgresql://concurso_3m97_user:oGMcdg48jfvuC835ioRXcRDldxY0nh4C@dpg-d68c1aa48b3s73ajp0b0-a.oregon-postgres.render.com/concurso_3m97" -ForegroundColor Gray
Write-Host "      RENDER_EXTERNAL_HOSTNAME=concurso-f16y.onrender.com" -ForegroundColor Gray
Write-Host "   2. O Render fará redeploy automático" -ForegroundColor White
Write-Host "   3. Teste o site em: https://concurso-f16y.onrender.com" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Delete o arquivo .env.production por segurança!" -ForegroundColor Yellow
