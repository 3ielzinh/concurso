# Módulo de Gerenciamento de Usuários

## Visão Geral

Este módulo foi criado para substituir o painel administrativo do Django, oferecendo uma interface moderna e completa para gestão de usuários da plataforma.

## Funcionalidades Principais

### 1. Listagem de Usuários
- **URL:** `/user-management/`
- **Recursos:**
  - Visualização de todos os usuários cadastrados
  - Pesquisa por nome, email ou username
  - Filtros por status (ativo/inativo)
  - Filtros por plano (premium/gratuito)
  - Filtros por data de cadastro
  - Paginação de resultados
  - Estatísticas em tempo real (total, ativos, premium, novos do mês)

### 2. Detalhes do Usuário
- **URL:** `/user-management/<user_id>/`
- **Informações exibidas:**
  - Dados pessoais e de contato
  - Status da conta
  - Informações de assinatura
  - Histórico de assinaturas
  - Estatísticas de estudo
  - Módulos com acesso permitido
  - Notas administrativas
  - Logs de atividade (últimos 20 registros)

### 3. Edição de Usuário
- **URL:** `/user-management/<user_id>/edit/`
- **Campos editáveis:**
  - Username, email, nome e sobrenome
  - Telefone
  - Status da conta (ativo/inativo)
  - Permissões (staff)
  - Plano premium
  - Datas de assinatura (início e término)
  - Meta de horas de estudo

### 4. Gerenciamento de Acesso a Módulos
- **URL:** `/user-management/<user_id>/module-access/`
- **Recursos:**
  - Seleção de categorias específicas que o usuário pode acessar
  - Campo de nível de acesso customizado
  - Observações sobre permissões
  - Se nenhuma categoria for selecionada, o usuário usa permissões do plano

### 5. Notas Administrativas
- **Adicionar:** `/user-management/<user_id>/add-note/`
- **Excluir:** `/user-management/notes/<note_id>/delete/`
- **Recursos:**
  - Adicionar notas sobre usuários
  - Marcar notas como importantes
  - Histórico completo de notas
  - Identificação do administrador que criou a nota

### 6. Redefinir Senha
- **URL:** `/user-management/<user_id>/reset-password/`
- **Recursos:**
  - Administradores podem redefinir senha de qualquer usuário
  - Validação de confirmação de senha
  - Log da ação

### 7. Ações Rápidas
- **Ativar/Desativar usuário:** POST para `/user-management/<user_id>/toggle-status/`
- **Excluir usuário:** `/user-management/<user_id>/delete/`
  - Confirmação obrigatória
  - Lista tudo que será excluído
  - Proteção contra exclusão do próprio admin ou de superusers

## Segurança e Permissões

### Acesso Restrito
- Apenas usuários com `is_staff=True` ou `is_superuser=True` podem acessar
- Proteções contra ações perigosas (ex: admin não pode excluir a si mesmo)
- Logs de todas as ações administrativas

### Logs de Atividade
O sistema registra automaticamente:
- Edições de informações
- Mudanças de acesso a módulos
- Redefinições de senha
- Ativação/desativação de contas

## Modelos de Dados

### UserModuleAccess
Controla quais módulos/categorias cada usuário tem acesso.

**Campos:**
- `user`: Usuário (OneToOne)
- `allowed_categories`: Categorias permitidas (ManyToMany)
- `custom_access_level`: Nível de acesso customizado
- `notes`: Observações internas

### UserAccessLog
Registra logs de atividade para monitoramento.

**Campos:**
- `user`: Usuário
- `action`: Descrição da ação
- `ip_address`: Endereço IP
- `user_agent`: User Agent do navegador
- `timestamp`: Data/hora da ação

### UserAdminNote
Notas administrativas sobre usuários.

**Campos:**
- `user`: Usuário sobre quem é a nota
- `admin`: Administrador que criou
- `note`: Texto da nota
- `is_important`: Flag de importância
- `created_at`: Data de criação

## Interface do Usuário

### Design Moderno
- Baseado no Bootstrap 5
- Modo escuro suportado
- Responsivo para mobile
- Ícones do Bootstrap Icons
- Badges coloridos para status

### Navegação
- Link no menu lateral: "Gestão de Usuários" (apenas para staff)
- Breadcrumbs e botões de voltar em todas as páginas
- Ações rápidas com ícones intuitivos

## Integração com Django Admin

Embora este módulo substitua a necessidade do Django Admin para gestão de usuários, os modelos ainda estão registrados no admin padrão para:
- Backup e acesso de emergência
- Integração com outras ferramentas
- Migrations e estrutura do banco

## Uso Recomendado

1. **Para Gestão Diária:** Use o módulo de Gerenciamento de Usuários
2. **Para Desenvolvimento:** Use o Django Admin quando necessário
3. **Para Produção:** Desabilite o Django Admin publicamente, mantenha apenas este módulo

## Próximos Passos Sugeridos

1. Adicionar exportação de dados de usuários (CSV/Excel)
2. Implementar envio de emails aos usuários
3. Adicionar estatísticas avançadas
4. Criar relatórios de uso por usuário
5. Implementar histórico de alterações detalhado
6. Adicionar bulk actions (ações em massa)

## Acesso

**URL Base:** `/user-management/`

**Menu Lateral:** "Gestão de Usuários" (visível apenas para staff/admins)

**Atalho de Teclado:** (a implementar)
