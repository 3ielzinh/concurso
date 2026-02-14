# 🔧 Guia de Administração de Usuários

## 📋 Como Acessar o Painel Admin

1. Acesse: **http://localhost:8000/admin/**
2. Faça login com suas credenciais de administrador
3. Clique em **"Usuários"** no menu lateral

---

## 👥 Gerenciamento de Usuários

### 🔍 Listagem de Usuários

O painel exibe:
- **Username** - Nome de usuário
- **Email** - E-mail do usuário
- **Nome Completo** - Nome completo (se preenchido)
- **Status da Assinatura** - Indicador visual colorido:
  - 🟢 **Verde** = Premium Ativo
  - 🟠 **Laranja** = Expira em menos de 7 dias
  - 🔴 **Vermelho** = Expirada
  - ⚪ **Cinza** = Gratuito
- **Data de Expiração** - Quando a assinatura termina
- **Staff** - Se é administrador
- **Data de Cadastro** - Quando se registrou

### ✏️ Editando um Usuário

Clique no username para editar. Você verá várias seções:

#### 1. **Informações Básicas**
- Username, senha, nome, sobrenome

#### 2. **Permissões**
- Status: ativo, staff, superuser
- Grupos e permissões específicas

#### 3. **📱 Informações de Contato**
- Telefone

#### 4. **👤 Perfil**
- Foto de perfil
- Biografia
- Meta de horas mensais de estudo

#### 5. **💎 Assinatura Premium** ⭐
Esta é a seção principal para controle de acesso:

- **✅ É Premium**
  - Marque para ativar o acesso premium
  - Desmarcado = usuário gratuito (acesso limitado)
  
- **📅 Início da Assinatura**
  - Data de início do plano premium
  
- **📅 Fim da Assinatura**
  - Data de expiração
  - Deixe em branco para assinatura vitalícia
  - Sistema verifica automaticamente se expirou

#### 6. **📊 Timestamps**
- Data de criação e última atualização

---

## ⚡ Ações em Massa

Selecione múltiplos usuários e use as ações:

### 💎 Ativar Premium (1 ano)
- Marca os usuários como premium
- Define início = hoje
- Define fim = hoje + 365 dias
- **Uso**: Ativar vários usuários de uma vez

### ❌ Remover Premium
- Remove status premium
- Define data de expiração como hoje
- **Uso**: Cancelamentos em massa

### 📅 Estender Assinatura (30 dias)
- Adiciona 30 dias à data de expiração atual
- Só funciona para usuários já premium
- **Uso**: Cortesias, renovações rápidas

---

## 🎯 Cenários Comuns

### Dar Acesso Premium a um Usuário

1. Abra o usuário no admin
2. Role até **"💎 Assinatura Premium"**
3. Marque **"✅ É Premium"**
4. Defina **"Início da Assinatura"** = data de hoje
5. Defina **"Fim da Assinatura"**:
   - Para 1 mês: hoje + 30 dias
   - Para 1 ano: hoje + 365 dias
   - Para vitalício: deixe em branco
6. Clique em **"Salvar"**

✅ **Resultado**: Usuário terá acesso a TODO o conteúdo premium imediatamente!

### Remover Acesso Premium

1. Abra o usuário
2. **Desmarque** "✅ É Premium"
3. Clique em **"Salvar"**

✅ **Resultado**: Usuário perde acesso ao conteúdo premium.

### Verificar Se Premium Está Funcionando

1. Faça login com o usuário
2. Vá para **"Módulos"** (http://localhost:8000/modules/categories/)
3. Se for premium: verá TODAS as categorias (incluindo as marcadas como premium)
4. Se não for premium: verá apenas categorias gratuitas + aviso de upgrade

---

## 🔄 Sincronização Automática

O sistema sincroniza automaticamente:

- **Admin → Aplicação**: Qualquer mudança no admin reflete instantaneamente
-  **Signals Django**: Quando você edita uma assinatura no módulo "Assinaturas", o perfil do usuário é atualizado automaticamente

### Comando Manual de Sincronização

Se houver inconsistências, rode:

```bash
python manage.py sync_subscriptions
```

Isso sincroniza todas as assinaturas do banco com os perfis de usuários.

---

## 📊 Painel de Assinaturas

Além do painel de usuários, você pode gerenciar assinaturas em:

**Admin → Assinaturas e Planos → Assinaturas**

Lá você pode:
- Ver todas as assinaturas ativas/canceladas/expiradas
- Criar novas assinaturas vinculadas a usuários
- Usar ações em massa:
  - Sincronizar com usuário
  - Ativar assinaturas
  - Cancelar assinaturas

---

## ⚠️ Importante

1. **Sempre marque "É Premium"** para liberar conteúdo
2. **Data de expiração em branco** = assinatura vitalícia
3. **Mudanças são instantâneas** - não precisa reiniciar o servidor
4. **Sincronização automática** - signals cuidam de tudo
5. **Se o usuário é Premium mas não vê conteúdo**: Verifique se a data de expiração não passou

---

## 🎨 Recursos Visuais no Admin

- ✅ Status coloridos para fácil identificação
- 📊 Indicadores de dias restantes
- ⚠️ Alertas para assinaturas próximas do vencimento
- 🔍 Filtros por status premium, staff, ativo
- 🔎 Busca por username, email, nome
- 📅 Ordenação por data de cadastro

---

## 🚀 Dicas

- Use filtros laterais para encontrar usuários rapidamente
- Ações em massa são mais eficientes para múltiplos usuários
- Verifique sempre o indicador de status antes de fazer mudanças
- Para testes, crie usuários de teste e alterne os status

---

**🎯 Qualquer dúvida, consulte este guia ou execute o comando sync_subscriptions!**
