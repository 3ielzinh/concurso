# MicroSaaS Concursos - Plataforma de Estudos

Sistema completo de organização e acompanhamento de estudos para concursos públicos e vestibulares, desenvolvido com Django e preparado para deploy no Render.com.

## 🎯 Características Principais

- ✅ Sistema de autenticação completo (registro, login, perfil)
- 📚 14 categorias de estudo (Policiais, Militares, Fiscais, Jurídicas, etc.)
- 📊 Dashboard com métricas em tempo real
- ⏱️ Registro de sessões de estudo
- 📈 Relatórios e gráficos de progresso
- 🗓️ Cronograma de estudos personalizável
- 🔥 Sistema de streak (dias consecutivos de estudo)
- 💎 Sistema de planos (Free e Pro)
- 🎨 Interface moderna com Bootstrap 5
- 🔐 Pronto para produção com segurança

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11+ / Django 4.2
- **Banco de Dados:** PostgreSQL
- **Frontend:** Bootstrap 5, Chart.js, Bootstrap Icons
- **Deploy:** Render.com
- **Servidor:** Gunicorn + WhiteNoise

## 📋 Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL 12 ou superior
- Git

## 🚀 Instalação Local

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd Cursos
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL local
DATABASE_URL=postgresql://usuario:senha@localhost:5432/concursos_db
```

### 5. Crie o banco de dados PostgreSQL

```bash
# Acesse o PostgreSQL
psql -U postgres

# Crie o banco
CREATE DATABASE concursos_db;
CREATE USER concursos_user WITH PASSWORD 'sua_senha';
ALTER ROLE concursos_user SET client_encoding TO 'utf8';
ALTER ROLE concursos_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE concursos_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE concursos_db TO concursos_user;
\q
```

### 6. Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 8. Popule dados iniciais (opcional)

```bash
python manage.py shell < populate_data.py
```

### 9. Execute o servidor

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## 📦 Deploy no Render.com

### 1. Prepare o repositório

Certifique-se de que todos os arquivos estão commitados:

```bash
git add .
git commit -m "Preparando para deploy"
git push origin main
```

### 2. Crie uma conta no Render

- Acesse: https://render.com
- Crie uma conta gratuita

### 3. Crie um PostgreSQL Database

1. No dashboard do Render, clique em "New +"
2. Selecione "PostgreSQL"
3. Configure:
   - Name: `concursos-db`
   - Database: `concursos_db`
   - User: `concursos_user`
   - Region: `Oregon (US West)` ou o mais próximo
4. Selecione o plano FREE
5. Clique em "Create Database"
6. **Copie a "Internal Database URL"** - você vai precisar dela

### 4. Crie um Web Service

1. No dashboard, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub/GitLab
4. Configure:
   - **Name:** `concursos-saas`
   - **Region:** Mesma do banco de dados
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn config.wsgi:application`

### 5. Configure as Variáveis de Ambiente

No Render, na seção "Environment", adicione:

```env
PYTHON_VERSION=3.11.0
SECRET_KEY=gere-uma-chave-secreta-forte-aqui
DEBUG=False
ALLOWED_HOSTS=concursos-saas.onrender.com
DATABASE_URL=cole-aqui-a-internal-database-url-do-passo-3
```

Para gerar uma SECRET_KEY segura:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Deploy

1. Clique em "Create Web Service"
2. Aguarde o build (5-10 minutos na primeira vez)
3. O Render executará automaticamente:
   - `pip install -r requirements.txt`
   - `python manage.py collectstatic`
   - `gunicorn config.wsgi`

### 7. Execute as migrações

Após o primeiro deploy, acesse o Shell do Render:

1. No dashboard do seu web service
2. Clique em "Shell" (canto superior direito)
3. Execute:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 8. Acesse sua aplicação

Seu app estará disponível em:
```
https://concursos-saas.onrender.com
```

## 🔧 Configurações Adicionais

### Domínio Customizado

1. No Render, vá em Settings > Custom Domain
2. Adicione seu domínio
3. Configure o DNS conforme instruções

### Backups Automáticos

O Render Free tier não inclui backups automáticos. Para produção:
- Upgrade para plano pago
- Ou configure backups manuais via pg_dump

### Monitoramento

O Render fornece:
- Logs em tempo real
- Métricas de CPU/Memória
- Health checks automáticos

## 📚 Estrutura do Projeto

```
Cursos/
├── config/                 # Configurações principais
│   ├── settings.py        # Settings Django
│   ├── urls.py            # URLs principais
│   └── wsgi.py            # WSGI config
├── accounts/              # App de autenticação
├── modules/               # App de módulos e disciplinas
├── metrics/               # App de métricas e relatórios
├── dashboard/             # App do dashboard
├── subscriptions/         # App de assinaturas
├── templates/             # Templates HTML
├── static/                # Arquivos estáticos
├── staticfiles/           # Arquivos estáticos coletados
├── manage.py              # Django management
├── requirements.txt       # Dependências Python
├── Procfile              # Config para Render
└── .env.example          # Exemplo de variáveis
```

## 🎨 Funcionalidades por Módulo

### Accounts (Autenticação)
- Registro de usuários
- Login/Logout
- Perfil editável
- Foto de perfil
- Meta de horas mensais

### Modules (Estudo)
- 14 categorias diferentes
- Módulos por categoria
- Disciplinas com horas estimadas
- Registro de sessões de estudo
- Cronograma semanal

### Metrics (Métricas)
- Gráficos de progresso
- Sequência de estudos (streak)
- Metas personalizadas
- Relatórios detalhados

### Dashboard
- Visão geral consolidada
- Estatísticas em tempo real
- Acesso rápido às categorias
- Sessões recentes

### Subscriptions (Planos)
- Plano Free (limitado)
- Plano Pro (completo)
- Controle de acesso por plano
- Preparado para integração de pagamento

## 🔐 Segurança

O projeto implementa:
- CSRF Protection
- SQL Injection Protection (ORM Django)
- XSS Protection
- Secure cookies (production)
- HTTPS redirect (production)
- Password hashing (PBKDF2)

## 🐛 Debug e Troubleshooting

### Problema: Erro ao conectar no banco

Verifique:
- DATABASE_URL está correto
- PostgreSQL está rodando
- Credenciais estão corretas

### Problema: Static files não carregam

Execute:
```bash
python manage.py collectstatic --noinput
```

### Problema: Migrations não aplicam

```bash
python manage.py migrate --run-syncdb
```

## 📈 Próximas Melhorias

- [ ] Integração com gateway de pagamento (Stripe/Mercado Pago)
- [ ] API REST para mobile app
- [ ] Exportação de relatórios em PDF
- [ ] Sistema de gamificação (badges, conquistas)
- [ ] Fórum de discussão
- [ ] Questões práticas por disciplina
- [ ] Simulados cronometrados
- [ ] Integração com calendário Google
- [ ] Notificações push
- [ ] App mobile (React Native)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é open source. Sinta-se livre para usar e modificar.

## 👨‍💻 Autor

Desenvolvido como MicroSaaS educacional para estudantes de concursos públicos.

## 🙏 Agradecimentos

- Django Framework
- Bootstrap Team
- Chart.js
- Render.com

---

**Nota:** Este é um projeto educacional. Para uso em produção com dados reais, considere adicionar testes automatizados, CI/CD e monitoramento avançado.
