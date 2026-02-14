"""
Script para popular o banco de dados com dados iniciais
Execute com: python manage.py shell < populate_data.py
"""

from django.contrib.auth import get_user_model
from modules.models import Category, Module, Subject
from subscriptions.models import Plan
from django.utils import timezone

User = get_user_model()

print("🚀 Iniciando população do banco de dados...")

# Criar Planos
print("\n📋 Criando planos...")
plans_data = [
    {
        'name': 'Gratuito',
        'plan_type': 'free',
        'description': 'Plano básico para começar seus estudos',
        'price': 0,
        'features': '''Acesso a 3 categorias
Registro de horas de estudo
Dashboard básico
Cronograma simples''',
        'max_categories': 3,
        'max_modules': 10,
        'has_premium_categories': False,
        'has_analytics': False,
        'has_export': False,
    },
    {
        'name': 'Pro',
        'plan_type': 'pro',
        'description': 'Acesso completo a todas as funcionalidades',
        'price': 29.90,
        'features': '''Acesso ilimitado a todas categorias
Relatórios avançados
Exportação de dados
Metas personalizadas
Estatísticas detalhadas
Suporte prioritário''',
        'max_categories': 999,
        'max_modules': 999,
        'has_premium_categories': True,
        'has_analytics': True,
        'has_export': True,
    }
]

for plan_data in plans_data:
    plan, created = Plan.objects.get_or_create(
        plan_type=plan_data['plan_type'],
        defaults=plan_data
    )
    if created:
        print(f"  ✅ Plano '{plan.name}' criado")
    else:
        print(f"  ℹ️  Plano '{plan.name}' já existe")

# Criar Categorias
print("\n📚 Criando categorias...")
categories_data = [
    {'name': 'policiais', 'description': 'Carreiras policiais (PF, PRF, PC, PM)', 'icon': 'shield-fill-check', 'color': 'primary', 'is_premium': False, 'order': 1},
    {'name': 'militares', 'description': 'Carreiras militares (Exército, Marinha, Aeronáutica)', 'icon': 'star-fill', 'color': 'success', 'is_premium': False, 'order': 2},
    {'name': 'fiscais', 'description': 'Carreiras fiscais (Receita Federal, Estadual)', 'icon': 'cash-coin', 'color': 'warning', 'is_premium': True, 'order': 3},
    {'name': 'juridicas', 'description': 'Carreiras jurídicas (OAB, Magistratura, MP)', 'icon': 'bank', 'color': 'danger', 'is_premium': True, 'order': 4},
    {'name': 'bancarias', 'description': 'Concursos bancários (BB, CEF, BNB)', 'icon': 'piggy-bank', 'color': 'info', 'is_premium': False, 'order': 5},
    {'name': 'educacao', 'description': 'Área de educação (Professor, Pedagogo)', 'icon': 'book', 'color': 'primary', 'is_premium': True, 'order': 6},
    {'name': 'saude', 'description': 'Área de saúde (Enfermagem, Medicina)', 'icon': 'hospital', 'color': 'danger', 'is_premium': True, 'order': 7},
    {'name': 'administrativa', 'description': 'Área administrativa (Assistente, Analista)', 'icon': 'briefcase', 'color': 'secondary', 'is_premium': False, 'order': 8},
    {'name': 'ti', 'description': 'Tecnologia da Informação', 'icon': 'laptop', 'color': 'info', 'is_premium': True, 'order': 9},
    {'name': 'engenharia', 'description': 'Engenharias diversas', 'icon': 'gear-fill', 'color': 'warning', 'is_premium': True, 'order': 10},
    {'name': 'fiscalizacao', 'description': 'Fiscalização e regulação', 'icon': 'clipboard-check', 'color': 'success', 'is_premium': True, 'order': 11},
    {'name': 'logistica', 'description': 'Logística e transporte', 'icon': 'truck', 'color': 'primary', 'is_premium': True, 'order': 12},
    {'name': 'legislativa', 'description': 'Poder legislativo (Câmara, Senado)', 'icon': 'building', 'color': 'secondary', 'is_premium': True, 'order': 13},
    {'name': 'enem_vestibular', 'description': 'ENEM e Vestibulares', 'icon': 'mortarboard-fill', 'color': 'info', 'is_premium': False, 'order': 14},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"  ✅ Categoria '{category.get_name_display()}' criada")
    else:
        print(f"  ℹ️  Categoria '{category.get_name_display()}' já existe")

# Criar alguns Módulos e Disciplinas de exemplo
print("\n📖 Criando módulos e disciplinas de exemplo...")

# Carreiras Policiais
cat_policiais = Category.objects.get(name='policiais')
modulo_pf, _ = Module.objects.get_or_create(
    category=cat_policiais,
    name='Polícia Federal - Agente',
    defaults={'description': 'Preparação para o concurso de Agente da Polícia Federal', 'order': 1}
)

disciplinas_pf = [
    {'name': 'Português', 'estimated_hours': 80},
    {'name': 'Raciocínio Lógico', 'estimated_hours': 60},
    {'name': 'Informática', 'estimated_hours': 40},
    {'name': 'Direito Constitucional', 'estimated_hours': 70},
    {'name': 'Direito Administrativo', 'estimated_hours': 60},
    {'name': 'Direito Penal', 'estimated_hours': 80},
    {'name': 'Legislação Especial', 'estimated_hours': 50},
]

for disc_data in disciplinas_pf:
    Subject.objects.get_or_create(
        module=modulo_pf,
        name=disc_data['name'],
        defaults={'estimated_hours': disc_data['estimated_hours'], 'order': disciplinas_pf.index(disc_data) + 1}
    )

print(f"  ✅ Módulo '{modulo_pf.name}' com {len(disciplinas_pf)} disciplinas")

# ENEM/Vestibular
cat_enem = Category.objects.get(name='enem_vestibular')
modulo_enem, _ = Module.objects.get_or_create(
    category=cat_enem,
    name='ENEM - Preparação Completa',
    defaults={'description': 'Todas as áreas do conhecimento para o ENEM', 'order': 1}
)

disciplinas_enem = [
    {'name': 'Matemática', 'estimated_hours': 100},
    {'name': 'Português', 'estimated_hours': 80},
    {'name': 'Redação', 'estimated_hours': 60},
    {'name': 'Geografia', 'estimated_hours': 60},
    {'name': 'História', 'estimated_hours': 60},
    {'name': 'Física', 'estimated_hours': 80},
    {'name': 'Química', 'estimated_hours': 80},
    {'name': 'Biologia', 'estimated_hours': 70},
    {'name': 'Literatura', 'estimated_hours': 40},
    {'name': 'Inglês', 'estimated_hours': 40},
]

for disc_data in disciplinas_enem:
    Subject.objects.get_or_create(
        module=modulo_enem,
        name=disc_data['name'],
        defaults={'estimated_hours': disc_data['estimated_hours'], 'order': disciplinas_enem.index(disc_data) + 1}
    )

print(f"  ✅ Módulo '{modulo_enem.name}' com {len(disciplinas_enem)} disciplinas")

# Carreiras Bancárias
cat_bancarias = Category.objects.get(name='bancarias')
modulo_bb, _ = Module.objects.get_or_create(
    category=cat_bancarias,
    name='Banco do Brasil - Escriturário',
    defaults={'description': 'Preparação para concurso do Banco do Brasil', 'order': 1}
)

disciplinas_bb = [
    {'name': 'Português', 'estimated_hours': 60},
    {'name': 'Matemática Financeira', 'estimated_hours': 80},
    {'name': 'Raciocínio Lógico', 'estimated_hours': 50},
    {'name': 'Informática', 'estimated_hours': 40},
    {'name': 'Conhecimentos Bancários', 'estimated_hours': 70},
    {'name': 'Atualidades', 'estimated_hours': 30},
]

for disc_data in disciplinas_bb:
    Subject.objects.get_or_create(
        module=modulo_bb,
        name=disc_data['name'],
        defaults={'estimated_hours': disc_data['estimated_hours'], 'order': disciplinas_bb.index(disc_data) + 1}
    )

print(f"  ✅ Módulo '{modulo_bb.name}' com {len(disciplinas_bb)} disciplinas")

print("\n✨ População do banco de dados concluída!")
print("\n📝 Resumo:")
print(f"   - {Plan.objects.count()} planos")
print(f"   - {Category.objects.count()} categorias")
print(f"   - {Module.objects.count()} módulos")
print(f"   - {Subject.objects.count()} disciplinas")
print("\n🎉 Pronto! Você pode começar a usar o sistema.")
