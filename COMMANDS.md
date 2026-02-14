# Comandos Úteis - MicroSaaS Concursos

## 🚀 Setup Inicial

### Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Desativar
deactivate
```

### Instalação
```bash
# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list

# Atualizar dependências
pip install --upgrade -r requirements.txt
```

## 💾 Banco de Dados

### PostgreSQL Local
```bash
# Criar banco
psql -U postgres
CREATE DATABASE concursos_db;
CREATE USER concursos_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE concursos_db TO concursos_user;
\q

# Conectar no banco
psql -U concursos_user -d concursos_db

# Listar tabelas
\dt

# Descrever tabela
\d nome_tabela

# Sair
\q
```

### Migrations
```bash
# Criar migrações
python manage.py makemigrations

# Ver SQL das migrações
python manage.py sqlmigrate nome_app 0001

# Aplicar migrações
python manage.py migrate

# Resetar migrações (CUIDADO!)
python manage.py migrate nome_app zero
python manage.py migrate

# Verificar status
python manage.py showmigrations
```

## 👤 Usuários

### Superusuário
```bash
# Criar superusuário
python manage.py createsuperuser

# Mudar senha de usuário
python manage.py changepassword nome_usuario
```

### Shell Interactive
```bash
# Abrir shell Django
python manage.py shell

# No shell:
from accounts.models import User
from modules.models import Category, StudySession

# Ver todos usuários
User.objects.all()

# Criar usuário
user = User.objects.create_user(
    username='teste',
    email='teste@email.com',
    password='senha123'
)

# Tornar premium
user.is_premium = True
user.save()

# Sair
exit()
```

## 🎨 Static Files

```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Sem confirmação
python manage.py collectstatic --noinput

# Limpar arquivos antigos
python manage.py collectstatic --clear --noinput
```

## 🔧 Desenvolvimento

### Server
```bash
# Rodar servidor de desenvolvimento
python manage.py runserver

# Em porta específica
python manage.py runserver 8080

# Acessível na rede local
python manage.py runserver 0.0.0.0:8000
```

### Debug
```bash
# Ver configurações
python manage.py diffsettings

# Verificar deploy checklist
python manage.py check --deploy

# Listar URLs
python manage.py show_urls  # Requer django-extensions
```

## 📊 Dados

### Popular Banco
```bash
# Executar script de população
python manage.py shell < populate_data.py

# Ou manualmente no shell
python manage.py shell
exec(open('populate_data.py').read())
```

### Backup e Restore
```bash
# Dump (backup) do banco
python manage.py dumpdata > backup.json

# Dump de um app específico
python manage.py dumpdata modules > modules_backup.json

# Restore
python manage.py loaddata backup.json

# Flush (LIMPA TUDO!)
python manage.py flush
```

## 🧪 Testes

```bash
# Rodar todos os testes
python manage.py test

# Testar app específico
python manage.py test accounts

# Testar com verbosidade
python manage.py test --verbosity=2

# Manter banco de teste
python manage.py test --keepdb
```

## 🔍 Debug e Troubleshooting

### Limpar Cache do Navegador
```
Ctrl + Shift + Delete (Chrome/Firefox)
Ou use aba anônima
```

### Recriar Migrations
```bash
# CUIDADO: Só em desenvolvimento!
# Deletar migrations antigas
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recriar
python manage.py makemigrations
python manage.py migrate
```

### Reset do Banco
```bash
# CUIDADO: Perde TODOS os dados!

# PostgreSQL
dropdb concursos_db
createdb concursos_db

# Ou via psql
psql -U postgres
DROP DATABASE concursos_db;
CREATE DATABASE concursos_db;
\q

# Django
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < populate_data.py
```

## 📦 Requirements

### Gerar requirements.txt
```bash
# Todas as dependências instaladas
pip freeze > requirements.txt

# Apenas as principais (pipreqs)
pip install pipreqs
pipreqs . --force
```

### Instalar pacote novo
```bash
# Instalar
pip install nome-do-pacote

# Adicionar ao requirements.txt
pip freeze | grep nome-do-pacote >> requirements.txt

# Ou manualmente
echo "nome-do-pacote==versao" >> requirements.txt
```

## 🚀 Deploy (Render.com)

### Via Dashboard
```
1. Conectar GitHub
2. Configurar variáveis
3. Deploy automático
```

### Via CLI (Render)
```bash
# Instalar CLI
npm install -g @render/cli

# Login
render login

# Deploy
render deploy
```

### Comandos no Shell do Render
```bash
# Acessar shell
# (Via Dashboard > Shell)

# Migrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Popular dados
python manage.py shell < populate_data.py

# Coletar static
python manage.py collectstatic --noinput
```

## 🔐 Segurança

### Gerar SECRET_KEY
```bash
# Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Ou no Django shell
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Verificar Segurança
```bash
python manage.py check --deploy
```

## 📝 Logs

### Development
```bash
# Django mostra no console automático
python manage.py runserver
```

### Production (Render)
```bash
# Ver logs em tempo real
# Dashboard > Logs (interface web)

# Filtrar erros
# Use filtro na interface: "error"
```

## 🔄 Git Commands

### Básico
```bash
# Status
git status

# Add
git add .
git add arquivo.py

# Commit
git commit -m "Mensagem descritiva"

# Push
git push origin main

# Pull
git pull origin main
```

### Branches
```bash
# Criar branch
git checkout -b feature/nova-funcionalidade

# Mudar de branch
git checkout main

# Merge
git checkout main
git merge feature/nova-funcionalidade

# Deletar branch
git branch -d feature/nova-funcionalidade
```

## 🛠️ Utilitários

### Ver Info do Sistema
```bash
# Versão Python
python --version

# Versão Django
python -m django --version

# Ou
python manage.py version

# Info do PostgreSQL
psql --version
```

### Limpar Cache Python
```bash
# Linux/Mac
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Windows PowerShell
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Filter "*.pyc" -Recurse -File | Remove-Item -Force
```

### Ambiente
```bash
# Ver variáveis de ambiente
python manage.py diffsettings

# Ver env atual
echo $DEBUG  # Linux/Mac
echo %DEBUG%  # Windows
```

## 📊 Queries Úteis (Django Shell)

```python
# Abrir shell
python manage.py shell

# Importar models
from accounts.models import User
from modules.models import Category, Module, Subject, StudySession, Progress
from metrics.models import StudyGoal, StudyStreak
from django.db.models import Sum, Count, Avg

# Ver total de usuários
User.objects.count()

# Ver usuários premium
User.objects.filter(is_premium=True)

# Total de horas de um usuário
user = User.objects.get(username='nome')
StudySession.objects.filter(user=user).aggregate(Sum('hours'))

# Sessões dos últimos 7 dias
from datetime import timedelta
from django.utils import timezone
date_7_days_ago = timezone.now().date() - timedelta(days=7)
StudySession.objects.filter(user=user, date__gte=date_7_days_ago)

# Disciplinas mais estudadas
StudySession.objects.values('subject__name').annotate(
    total=Sum('hours')
).order_by('-total')[:10]

# Usuários mais ativos
StudySession.objects.values('user__username').annotate(
    total=Sum('hours')
).order_by('-total')[:10]
```

## 🎯 Atalhos

### Windows
```bash
# Ativar env e rodar server
venv\Scripts\activate && python manage.py runserver

# Migrations completas
python manage.py makemigrations && python manage.py migrate

# Limpar cache e rodar
rmdir /s /q __pycache__ && python manage.py runserver
```

### Linux/Mac
```bash
# Ativar env e rodar server
source venv/bin/activate && python manage.py runserver

# Migrations completas
python manage.py makemigrations && python manage.py migrate

# Limpar cache e rodar
find . -name "*.pyc" -delete && python manage.py runserver
```

## 📚 Documentação Rápida

```bash
# Ver help de comando
python manage.py help
python manage.py help migrate

# Ver estrutura do projeto
tree  # Linux/Mac
tree /f  # Windows
```

## 🔥 Pro Tips

### Alias (Linux/Mac)
```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
alias djrun="python manage.py runserver"
alias djmig="python manage.py makemigrations && python manage.py migrate"
alias djshell="python manage.py shell"
alias djtest="python manage.py test"

# Usar
djrun
djmig
```

### PowerShell Profile (Windows)
```powershell
# Editar profile
notepad $PROFILE

# Adicionar:
function djrun { python manage.py runserver }
function djmig { python manage.py makemigrations; python manage.py migrate }
function djshell { python manage.py shell }

# Usar
djrun
djmig
```

---

**💡 Dica:** Mantenha este arquivo aberto enquanto desenvolve. Copie e cole os comandos conforme necessário!
