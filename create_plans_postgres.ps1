# Script para criar planos no banco de producao do Render
# Execute com: .\create_plans_postgres.ps1

Write-Host "CRIANDO PLANOS NO POSTGRESQL (RENDER)" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Gray

# Fazer backup do .env
Write-Host "`nFazendo backup das configuracoes..." -ForegroundColor Yellow
Copy-Item .env .env.backup -Force

# Configurar para usar PostgreSQL do Render
Write-Host "`nConfigurando PostgreSQL do Render..." -ForegroundColor Yellow
$envContent = Get-Content .env
$envContent = $envContent -replace 'DATABASE_URL=.*', 'DATABASE_URL=postgresql://concurso_3m97_user:oGMcdg48jfvuC835ioRXcRDldxY0nh4C@dpg-d68c1aa48b3s73ajp0b0-a.oregon-postgres.render.com/concurso_3m97'
$envContent | Set-Content .env

try {
    # Executar o script de criacao de planos
    Write-Host "`nExecutando script de criacao de planos..." -ForegroundColor Cyan
    python create_plans.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nPlanos criados com sucesso no PostgreSQL!" -ForegroundColor Green
    } else {
        Write-Host "`nErro ao criar planos!" -ForegroundColor Red
    }
    
} catch {
    Write-Host "`nErro durante execucao: $_" -ForegroundColor Red
} finally {
    # Restaurar configuracao local
    Write-Host "`nRestaurando configuracao local..." -ForegroundColor Yellow
    Copy-Item .env.backup .env -Force
    Remove-Item .env.backup -Force
    Write-Host "Configuracao local restaurada" -ForegroundColor Green
}

Write-Host "`n" -NoNewline
Write-Host ("=" * 60) -ForegroundColor Gray
Write-Host "CONCLUIDO" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Gray

Write-Host "`nVerifique os planos em:" -ForegroundColor Yellow
Write-Host "   https://concurso-f16y.onrender.com/subscriptions/plans/" -ForegroundColor White
Write-Host "`nAcesse o admin em:" -ForegroundColor Yellow
Write-Host "   https://concurso-f16y.onrender.com/admin/" -ForegroundColor White
Write-Host "   Username: admin" -ForegroundColor Gray
Write-Host "   Password: Admin@2026" -ForegroundColor Gray
