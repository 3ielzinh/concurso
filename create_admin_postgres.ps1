# Script para criar superusuario no PostgreSQL do Render

Write-Host "Criando superusuario no PostgreSQL do Render..." -ForegroundColor Cyan
Write-Host ""

# 1. Backup do .env atual
Write-Host "Fazendo backup do .env local..." -ForegroundColor Yellow
Copy-Item .env .env.backup -Force
Write-Host "Backup criado" -ForegroundColor Green
Write-Host ""

# 2. Criar .env.production temporario
Write-Host "Configurando conexao com PostgreSQL..." -ForegroundColor Yellow
$envContent = @"
SECRET_KEY=django-insecure-temp-key
DEBUG=False
ALLOWED_HOSTS=localhost
DATABASE_URL=postgresql://concurso_3m97_user:oGMcdg48jfvuC835ioRXcRDldxY0nh4C@dpg-d68c1aa48b3s73ajp0b0-a.oregon-postgres.render.com/concurso_3m97
RENDER_EXTERNAL_HOSTNAME=concurso-f16y.onrender.com
"@
$envContent | Out-File -FilePath .env -Encoding utf8 -NoNewline
Write-Host "Conexao configurada" -ForegroundColor Green
Write-Host ""

# 3. Criar superusuario
Write-Host "Criando superusuario no PostgreSQL..." -ForegroundColor Yellow
Write-Host ""

$createUserScript = @"
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
if User.objects.filter(username=username).exists():
    print('Usuario admin ja existe no PostgreSQL')
    user = User.objects.get(username=username)
    print(f'Email: {user.email}')
else:
    user = User.objects.create_superuser(
        username='admin',
        email='admin@concurso.com',
        password='Admin@2026',
        first_name='Admin',
        last_name='Sistema'
    )
    print('Superusuario criado com sucesso no PostgreSQL')
    print('Username: admin')
    print('Email: admin@concurso.com')
    print('Password: Admin@2026')
"@

$createUserScript | python manage.py shell

Write-Host ""

# 4. Restaurar .env local
Write-Host "Restaurando configuracao local..." -ForegroundColor Yellow
Copy-Item .env.backup .env -Force
Remove-Item .env.backup -Force
Write-Host "Configuracao local restaurada" -ForegroundColor Green
Write-Host ""

Write-Host "CONCLUIDO" -ForegroundColor Green
Write-Host ""
Write-Host "Credenciais do Superusuario:" -ForegroundColor Cyan
Write-Host "URL Admin: https://concurso-f16y.onrender.com/admin/" -ForegroundColor White
Write-Host "Username: admin" -ForegroundColor White
Write-Host "Password: Admin@2026" -ForegroundColor White

