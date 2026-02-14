# -*- coding: utf-8 -*-
"""
Script para criar planos baseados nos modulos existentes
Execute com: python -c "exec(open('create_plans.py').read())"
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from modules.models import Module, Category
from subscriptions.models import Plan, Subscription

print("Recriando estrutura de planos...")

# Deletar assinaturas e planos antigos
print("\nRemovendo assinaturas antigas...")
Subscription.objects.all().delete()
print("  Assinaturas antigas removidas")

print("\nRemovendo planos antigos...")
Plan.objects.all().delete()
print("  Planos antigos removidos")

# Criar plano gratuito basico
print("\nCriando plano GRATUITO...")
plan_free = Plan.objects.create(
    name='Plano Gratuito',
    plan_type='free',
    description='Plano basico para comecar seus estudos',
    price=0,
    features='''Acesso a modulos gratuitos selecionados
Registro de horas de estudo
Dashboard basico
Cronograma simples''',
    max_categories=2,
    max_modules=2,
    has_premium_categories=False,
    has_analytics=False,
    has_export=False,
)
print(f"  {plan_free.name} criado - R$ {plan_free.price}")

# Criar plano CARREIRA POLICIAL
print("\nCriando plano CARREIRA POLICIAL...")
cat_police = Category.objects.get(name='policiais')
modules_police = Module.objects.filter(category=cat_police)
plan_police = Plan.objects.create(
    name='Plano Carreira Policial',
    plan_type='police',
    description='Acesso completo a todos os modulos para carreiras policiais',
    price=49.90,
    features='''Todos os modulos de Carreiras Policiais
Material para PF, PRF, PC, PM
Relatorios de desempenho
Cronograma personalizado
Estatisticas detalhadas
Suporte prioritario''',
    max_categories=1,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_police.modules.set(modules_police)
print(f"  {plan_police.name} criado - R$ {plan_police.price} ({modules_police.count()} modulos)")

# Criar plano CARREIRA BANCARIA
print("\nCriando plano CARREIRA BANCARIA...")
cat_bank = Category.objects.get(name='bancarias')
modules_bank = Module.objects.filter(category=cat_bank)
plan_bank = Plan.objects.create(
    name='Plano Carreira Bancaria',
    plan_type='bank',
    description='Acesso completo a todos os modulos para carreiras bancarias',
    price=39.90,
    features='''Todos os modulos de Carreiras Bancarias
Material para BB, CEF, BNB
Relatorios de desempenho
Cronograma personalizado
Estatisticas detalhadas
Suporte prioritario''',
    max_categories=1,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_bank.modules.set(modules_bank)
print(f"  {plan_bank.name} criado - R$ {plan_bank.price} ({modules_bank.count()} modulos)")

# Criar plano ENEM/VESTIBULAR
print("\nCriando plano ENEM/VESTIBULAR...")
cat_enem = Category.objects.get(name='enem_vestibular')
modules_enem = Module.objects.filter(category=cat_enem)
plan_enem = Plan.objects.create(
    name='Plano ENEM/Vestibular',
    plan_type='enem',
    description='Preparacao completa para ENEM e vestibulares',
    price=44.90,
    features='''Todos os modulos ENEM/Vestibular
Todas as areas do conhecimento
Relatorios de desempenho
Cronograma personalizado
Simulados e estatisticas
Suporte prioritario''',
    max_categories=1,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_enem.modules.set(modules_enem)
print(f"  {plan_enem.name} criado - R$ {plan_enem.price} ({modules_enem.count()} modulos)")

# Criar plano PRO - ACESSO TOTAL
print("\nCriando plano PRO - ACESSO TOTAL...")
all_modules = Module.objects.all()
plan_pro = Plan.objects.create(
    name='Plano PRO - Acesso Total',
    plan_type='pro',
    description='Acesso ilimitado a TODOS os modulos e categorias',
    price=99.90,
    features='''TODOS os modulos disponiveis
TODAS as categorias
Carreiras Policiais
Carreiras Bancarias
ENEM/Vestibular
Carreiras Militares
Carreiras Fiscais
Carreiras Juridicas
Relatorios avancados
Exportacao de dados
Metas personalizadas
Estatisticas completas
Suporte VIP''',
    max_categories=999,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_pro.modules.set(all_modules)
print(f"  {plan_pro.name} criado - R$ {plan_pro.price} ({all_modules.count()} modulos)")

# Resumo final
print("\n" + "="*60)
print("Estrutura de planos criada com sucesso!")
print("="*60)
print("\nRESUMO DOS PLANOS:")
print("-" * 60)

for plan in Plan.objects.all().order_by('price'):
    module_count = plan.modules.count()
    print(f"\n{plan.name}")
    print(f"  Preco: R$ {plan.price}")
    print(f"  Modulos: {module_count}")
    if module_count > 0:
        print(f"  Lista de modulos:")
        for module in plan.modules.all():
            print(f"     - {module.name}")
    print(f"  Recursos: {len([f for f in plan.features.split('\\n') if f.strip()])}")

print("\n" + "="*60)
print("Pronto! Os planos estao configurados.")
print("="*60)

# Criar plano gratuito básico
print("\n📋 Criando plano GRATUITO...")
plan_free = Plan.objects.create(
    name='Plano Gratuito',
    plan_type='free',
    description='Plano básico para começar seus estudos',
    price=0,
    features='''Acesso a módulos gratuitos selecionados
Registro de horas de estudo
Dashboard básico
Cronograma simples''',
    max_categories=2,
    max_modules=2,
    has_premium_categories=False,
    has_analytics=False,
    has_export=False,
)
print(f"  ✅ {plan_free.name} criado - R$ {plan_free.price}")

# Criar plano CARREIRA POLICIAL
print("\n👮 Criando plano CARREIRA POLICIAL...")
cat_police = Category.objects.get(name='policiais')
modules_police = Module.objects.filter(category=cat_police)
plan_police = Plan.objects.create(
    name='Plano Carreira Policial',
    plan_type='police',
    description='Acesso completo a todos os módulos para carreiras policiais',
    price=49.90,
    features='''Todos os módulos de Carreiras Policiais
Material para PF, PRF, PC, PM
Relatórios de desempenho
Cronograma personalizado
Estatísticas detalhadas
Suporte prioritário''',
    max_categories=1,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_police.modules.set(modules_police)
print(f"  ✅ {plan_police.name} criado - R$ {plan_police.price} ({modules_police.count()} módulos)")

# Criar plano CARREIRA BANCÁRIA
print("\n🏦 Criando plano CARREIRA BANCÁRIA...")
cat_bank = Category.objects.get(name='bancarias')
modules_bank = Module.objects.filter(category=cat_bank)
plan_bank = Plan.objects.create(
    name='Plano Carreira Bancária',
    plan_type='bank',
    description='Acesso completo a todos os módulos para carreiras bancárias',
    price=39.90,
    features='''Todos os módulos de Carreiras Bancárias
Material para BB, CEF, BNB
Relatórios de desempenho
Cronograma personalizado
Estatísticas detalhadas
Suporte prioritário''',
    max_categories=1,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_bank.modules.set(modules_bank)
print(f"  ✅ {plan_bank.name} criado - R$ {plan_bank.price} ({modules_bank.count()} módulos)")

# Criar plano ENEM/VESTIBULAR
print("\n🎓 Criando plano ENEM/VESTIBULAR...")
cat_enem = Category.objects.get(name='enem_vestibular')
modules_enem = Module.objects.filter(category=cat_enem)
plan_enem = Plan.objects.create(
    name='Plano ENEM/Vestibular',
    plan_type='enem',
    description='Preparação completa para ENEM e vestibulares',
    price=44.90,
    features='''Todos os módulos ENEM/Vestibular
Todas as áreas do conhecimento
Relatórios de desempenho
Cronograma personalizado
Simulados e estatísticas
Suporte prioritário''',
    max_categories=1,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_enem.modules.set(modules_enem)
print(f"  ✅ {plan_enem.name} criado - R$ {plan_enem.price} ({modules_enem.count()} módulos)")

# Criar plano PRO - ACESSO TOTAL
print("\n⭐ Criando plano PRO - ACESSO TOTAL...")
all_modules = Module.objects.all()
plan_pro = Plan.objects.create(
    name='Plano PRO - Acesso Total',
    plan_type='pro',
    description='Acesso ilimitado a TODOS os módulos e categorias',
    price=99.90,
    features='''✅ TODOS os módulos disponíveis
✅ TODAS as categorias
✅ Carreiras Policiais
✅ Carreiras Bancárias
✅ ENEM/Vestibular
✅ Carreiras Militares
✅ Carreiras Fiscais
✅ Carreiras Jurídicas
✅ Relatórios avançados
✅ Exportação de dados
✅ Metas personalizadas
✅ Estatísticas completas
✅ Suporte VIP''',
    max_categories=999,
    max_modules=999,
    has_premium_categories=True,
    has_analytics=True,
    has_export=True,
)
plan_pro.modules.set(all_modules)
print(f"  ✅ {plan_pro.name} criado - R$ {plan_pro.price} ({all_modules.count()} módulos)")

# Resumo final
print("\n" + "="*60)
print("✨ Estrutura de planos criada com sucesso!")
print("="*60)
print("\n📊 RESUMO DOS PLANOS:")
print("-" * 60)

for plan in Plan.objects.all().order_by('price'):
    module_count = plan.modules.count()
    print(f"\n{plan.name}")
    print(f"  💰 Preço: R$ {plan.price}")
    print(f"  📚 Módulos: {module_count}")
    if module_count > 0:
        print(f"  📖 Lista de módulos:")
        for module in plan.modules.all():
            print(f"     - {module.name}")
    print(f"  🔑 Recursos: {plan.features.count(chr(10))} recursos")

print("\n" + "="*60)
print("🎉 Pronto! Os planos estão configurados.")
print("="*60)
