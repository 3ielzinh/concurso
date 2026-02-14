# Guia Rápido de Deploy - Render.com

## 📋 Checklist Pré-Deploy

- [ ] Código commitado no GitHub/GitLab
- [ ] requirements.txt atualizado
- [ ] Procfile criado
- [ ] .env.example atualizado
- [ ] README.md completo

## 🚀 Passo a Passo

### 1. Criar Banco de Dados PostgreSQL

```
1. Dashboard > New > PostgreSQL
2. Name: concursos-db
3. Plan: Free
4. Create Database
5. COPIAR "Internal Database URL"
```

### 2. Criar Web Service

```
1. Dashboard > New > Web Service
2. Conectar repositório GitHub
3. Configurar:
   - Name: concursos-saas
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn config.wsgi:application
```

### 3. Variáveis de Ambiente

```env
PYTHON_VERSION=3.11.0
SECRET_KEY=<gerar-com-django>
DEBUG=False
ALLOWED_HOSTS=concursos-saas.onrender.com
DATABASE_URL=<internal-database-url-do-passo-1>
```

**Gerar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Após Deploy

No Shell do Render:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < populate_data.py
```

### 5. Testar

```
https://concursos-saas.onrender.com
https://concursos-saas.onrender.com/admin
```

## ⚠️ Problemas Comuns

### Static files não carregam
```bash
python manage.py collectstatic --noinput
```

### Erro de migração
```bash
python manage.py migrate --run-syncdb
```

### Database connection error
- Verificar DATABASE_URL
- Verificar se o banco está rodando
- Verificar whitelist de IPs

## 📊 Monitoramento

- Logs: Dashboard > Logs
- Metrics: Dashboard > Metrics
- Health: Render faz health checks automáticos

## 🔄 Próximos Deploys

Render faz auto-deploy quando você faz push para a branch configurada (geralmente `main`).

## 📞 Suporte

- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com
