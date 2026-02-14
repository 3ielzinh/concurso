# Arquitetura do MicroSaaS Concursos

## 📐 Visão Geral da Arquitetura

Este documento descreve a arquitetura técnica do sistema, decisões de design e organização do código.

## 🏗️ Estrutura Modular

O projeto segue uma arquitetura modular baseada em apps Django, cada um com responsabilidade específica:

```
┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │
│  (Templates, Static Files, Bootstrap)   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          APPLICATION LAYER              │
│    (Views, URLs, Forms, Business Logic) │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ accounts │  │dashboard │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ modules  │  │ metrics  │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐                         │
│  │subscrip. │                         │
│  └──────────┘                         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│            DATA LAYER                   │
│   (Models, ORM, Database Layer)         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         POSTGRESQL DATABASE             │
└─────────────────────────────────────────┘
```

## 📦 Apps e Responsabilidades

### 1. **accounts** - Autenticação e Perfil
**Responsabilidade:** Gerenciar usuários, autenticação e perfis

**Models:**
- `User` (AbstractUser customizado)
  - Campos adicionais: profile_picture, bio, study_goal_hours
  - Campos de assinatura: is_premium, subscription_start/end
  - Método: `has_active_subscription`

**Views:**
- `UserRegisterView` - Registro de novos usuários
- `UserLoginView` - Autenticação
- `UserLogoutView` - Logout
- `ProfileView` - Edição de perfil

**URLs:**
- `/accounts/register/`
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/profile/`

### 2. **modules** - Módulos de Estudo
**Responsabilidade:** Gerenciar categorias, módulos, disciplinas e sessões de estudo

**Models:**
- `Category` - Categorias principais (14 tipos)
- `Module` - Módulos dentro de cada categoria
- `Subject` - Disciplinas específicas
- `StudySession` - Sessões de estudo registradas
- `Progress` - Progresso do usuário por disciplina
- `StudySchedule` - Cronograma semanal

**Relações:**
```
Category (1) ─── (N) Module (1) ─── (N) Subject
                                         │
                                         │ (1)
                                         │
User (1) ─── (N) StudySession ─── (N) Subject
     │
     └─── (N) Progress ─── (1) Subject
     │
     └─── (N) StudySchedule ─── (1) Subject
```

**Views:**
- `CategoryListView` - Lista categorias
- `ModuleListView` - Lista módulos de uma categoria
- `SubjectDetailView` - Detalhes de disciplina + progresso
- CRUD completo para StudySession
- CRUD completo para StudySchedule

### 3. **metrics** - Métricas e Relatórios
**Responsabilidade:** Calcular e exibir métricas de estudo

**Models:**
- `StudyGoal` - Metas personalizadas de estudo
- `StudyStreak` - Sequência de dias estudando

**Views:**
- `MetricsReportView` - Relatório completo com:
  - Total de horas (all time, semanal, mensal)
  - Progresso por categoria
  - Gráficos de evolução
  - Metas ativas

**Cálculos:**
- Agregação de horas usando Django ORM
- Cálculo de percentuais de progresso
- Atualização automática de streaks

### 4. **dashboard** - Painel Principal
**Responsabilidade:** Visão consolidada do progresso do usuário

**Views:**
- `DashboardHomeView` - Dashboard principal com:
  - Cards de estatísticas
  - Progresso geral
  - Sessões recentes
  - Acesso rápido a categorias
  - Status da assinatura

**Lógica:**
- Agrega dados de múltiplos apps
- Apresenta overview consolidado
- Ponto de entrada após login

### 5. **subscriptions** - Planos e Assinaturas
**Responsabilidade:** Gerenciar planos e controle de acesso

**Models:**
- `Plan` - Planos disponíveis (Free, Pro)
  - Controle de recursos por plano
  - Features textuais
- `Subscription` - Assinatura do usuário
  - Status: active, cancelled, expired, trial
  - Datas de início/fim
  - Auto-renew

**Views:**
- `PlansListView` - Lista planos disponíveis
- `MySubscriptionView` - Assinatura atual do usuário
- `UpgradeView` - Upgrade (placeholder para pagamento)

**Controle de Acesso:**
```python
# Exemplo de verificação
if not user.has_active_subscription:
    categories = categories.filter(is_premium=False)
```

## 🔐 Sistema de Autenticação

### Custom User Model
Utilizamos `AbstractUser` para estender o modelo padrão:

```python
class User(AbstractUser):
    # Campos personalizados
    email = unique
    phone, profile_picture, bio
    study_goal_hours
    is_premium, subscription_start, subscription_end
```

### Login Flow
```
1. Usuário acessa /accounts/login/
2. LoginView processa credenciais
3. Django cria sessão
4. Redirect para dashboard
5. Middleware AuthenticationMiddleware valida requests
```

### Permission System
```python
# View protegida
class ProtectedView(LoginRequiredMixin, View):
    ...

# Template
{% if user.is_authenticated %}
    # conteúdo protegido
{% endif %}
```

## 🎨 Frontend Architecture

### Template Hierarchy
```
base.html (layout principal + sidebar)
    ├── accounts/*.html (login, register, profile)
    ├── dashboard/home.html
    ├── modules/*.html (categories, modules, subjects)
    ├── metrics/report.html
    └── subscriptions/*.html (plans, my_subscription)
```

### Component Structure
- **Sidebar:** Navegação fixa (component reutilizável)
- **Topbar:** Header com menu de usuário
- **Content Area:** Conteúdo dinâmico
- **Cards:** Componentes de estatísticas
- **Forms:** Bootstrap + Crispy Forms

### CSS Framework
- Bootstrap 5.3.2
- Bootstrap Icons 1.11.1
- Custom CSS para sidebar e cards
- Responsivo mobile-first

### JavaScript
- Chart.js 4.4.0 para gráficos
- Bootstrap JS bundle para interatividade
- Minimal custom JavaScript

## 💾 Modelo de Dados

### Principais Entidades

#### User (accounts.User)
```python
- id (PK)
- username, email, password (herdados)
- first_name, last_name
- profile_picture, phone, bio
- study_goal_hours
- is_premium, subscription_start, subscription_end
- created_at, updated_at
```

#### Category (modules.Category)
```python
- id (PK)
- name (choices: 14 categorias)
- description, icon, color
- is_premium (boolean)
- order, is_active
```

#### StudySession (modules.StudySession)
```python
- id (PK)
- user_id (FK → User)
- subject_id (FK → Subject)
- date, hours
- notes, completed
- created_at, updated_at
```

#### Progress (modules.Progress)
```python
- id (PK)
- user_id (FK → User)
- subject_id (FK → Subject)
- percentage, total_hours
- is_completed, last_studied
- unique_together: [user, subject]
```

### Índices e Performance
```python
# Índices automáticos em:
- Foreign Keys
- unique_together constraints
- ordering fields

# Otimizações:
- select_related() para FKs
- prefetch_related() para M2M
- aggregate() para cálculos
```

## 🔄 Business Logic

### Registro de Sessão de Estudo
```python
1. Usuário preenche formulário
2. View valida dados
3. Cria StudySession
4. Atualiza/Cria Progress:
   - Calcula total_hours (aggregate)
   - Calcula percentage
   - Marca is_completed se >= 100%
   - Atualiza last_studied
5. Atualiza StudyStreak:
   - Verifica data da última sessão
   - Incrementa ou reseta streak
   - Atualiza longest_streak
6. Redirect para dashboard
```

### Controle de Acesso por Plano
```python
# View
queryset = Subject.objects.filter(is_active=True)
if not user.has_active_subscription:
    queryset = queryset.filter(
        module__category__is_premium=False
    )

# Model property
@property
def has_active_subscription(self):
    if not self.is_premium or not self.subscription_end:
        return False
    return self.subscription_end >= timezone.now().date()
```

### Cálculo de Métricas
```python
# Total de horas
total = StudySession.objects.filter(
    user=user
).aggregate(Sum('hours'))['hours__sum'] or 0

# Progresso por categoria
Progress.objects.filter(
    user=user,
    subject__module__category=category
).aggregate(
    avg_percentage=Sum('percentage'),
    total_hours=Sum('total_hours')
)
```

## 🚀 Deploy e Infraestrutura

### Stack de Produção
```
┌──────────────┐
│  Render.com  │ (Platform)
└──────────────┘
       │
       ├─ Web Service (Python)
       │  └─ Gunicorn + Django
       │     └─ WhiteNoise (static files)
       │
       └─ PostgreSQL Database
          └─ Managed by Render
```

### Environment Variables
```env
PYTHON_VERSION=3.11.0
SECRET_KEY=<generated>
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
DATABASE_URL=postgresql://...
```

### Static Files
```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise para servir estáticos
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

### Database
- PostgreSQL 12+
- Production: Render Managed PostgreSQL
- Development: Local PostgreSQL
- ORM: Django ORM (sem SQL raw)

## 🔒 Segurança

### Implementações
```python
# CSRF Protection (ativo por padrão)
{% csrf_token %}

# SQL Injection (ORM protege)
User.objects.filter(username=username)  # Safe

# XSS Protection (template escaping)
{{ user_input }}  # Auto-escaped

# Password Hashing
PBKDF2 algorithm (Django default)

# HTTPS (production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📈 Escalabilidade

### Considerações Atuais
- Database: PostgreSQL (vertical scaling)
- Static Files: WhiteNoise (CDN ready)
- Sessions: Database-backed
- Media: Local storage (S3 ready)

### Próximos Passos
- [ ] Cache layer (Redis)
- [ ] CDN para static/media (AWS S3 + CloudFront)
- [ ] Celery para tasks assíncronas
- [ ] Load balancer

## 🧪 Testing Strategy (Futuro)

### Sugestões
```python
# Unit tests
tests/test_models.py
tests/test_views.py
tests/test_forms.py

# Integration tests
tests/test_study_flow.py
tests/test_authentication.py

# Coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 Code Standards

### Python
- PEP 8 compliant
- Type hints (futuro)
- Docstrings para funções críticas
- Max line length: 120

### Django
- Class-based views
- Forms com Crispy Forms
- Admin customizado
- Signals para ações automáticas (futuro)

### Templates
- DRY principle
- Componentização
- Semantic HTML5
- Acessibilidade (WCAG)

## 🔄 CI/CD (Futuro)

### Pipeline Sugerido
```yaml
# .github/workflows/django.yml
- Checkout code
- Setup Python
- Install dependencies
- Run migrations (check)
- Run tests
- Coverage report
- Deploy to Render (auto)
```

## 📊 Monitoramento

### Logs
```python
# Django logging
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

### Metrics (Render)
- Request rate
- Response time
- Error rate
- Memory usage
- CPU usage

## 🎯 Performance Tips

### Database
```python
# Usar select_related para FKs
StudySession.objects.select_related(
    'user', 'subject', 'subject__module'
)

# Usar prefetch_related para reverse FKs
Category.objects.prefetch_related('modules__subjects')

# Aggregate em vez de loops
.aggregate(Sum('hours'))
```

### Queries
```python
# Evitar N+1
# Ruim:
for session in sessions:
    print(session.subject.name)

# Bom:
sessions = sessions.select_related('subject')
for session in sessions:
    print(session.subject.name)
```

### Templates
```python
# Cache fragments (futuro)
{% load cache %}
{% cache 500 sidebar %}
    # sidebar content
{% endcache %}
```

## 🔮 Roadmap Técnico

### Curto Prazo
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Error tracking (Sentry)

### Médio Prazo
- [ ] API REST (Django REST Framework)
- [ ] WebSockets (Django Channels) para notificações
- [ ] Cache layer (Redis)
- [ ] Task queue (Celery)

### Longo Prazo
- [ ] Microservices architecture
- [ ] Elasticsearch para busca
- [ ] ML para recomendações de estudo
- [ ] Mobile app (React Native + API)

---

Esta arquitetura foi projetada para ser:
- 📦 **Modular:** Fácil adicionar novos apps
- 🔧 **Manutenível:** Código organizado e documentado
- 📈 **Escalável:** Preparado para crescimento
- 🔒 **Seguro:** Seguindo best practices Django
- 🚀 **Performático:** Otimizações de query e assets
