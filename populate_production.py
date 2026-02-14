# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from modules.models import Category, Module, Subject
from subscriptions.models import Plan, Subscription

User = get_user_model()

print("Populando banco de producao...")

# Criar Categorias
print("\nCriando categorias...")
categories_data = [
    {'name': 'policiais', 'description': 'Carreiras policiais (PF, PRF, PC, PM)', 'icon': 'shield-fill-check', 'color': 'primary', 'is_premium': False, 'order': 1},
    {'name': 'militares', 'description': 'Carreiras militares (Exercito, Marinha, Aeronautica)', 'icon': 'star-fill', 'color': 'success', 'is_premium': False, 'order': 2},
    {'name': 'fiscais', 'description': 'Carreiras fiscais (Receita Federal, Estadual)', 'icon': 'cash-coin', 'color': 'warning', 'is_premium': True, 'order': 3},
    {'name': 'juridicas', 'description': 'Carreiras juridicas (OAB, Magistratura, MP)', 'icon': 'bank', 'color': 'danger', 'is_premium': True, 'order': 4},
    {'name': 'bancarias', 'description': 'Concursos bancarios (BB, CEF, BNB)', 'icon': 'piggy-bank', 'color': 'info', 'is_premium': False, 'order': 5},
    {'name': 'educacao', 'description': 'Area de educacao (Professor, Pedagogo)', 'icon': 'book', 'color': 'primary', 'is_premium': True, 'order': 6},
    {'name': 'saude', 'description': 'Area de saude (Enfermagem, Medicina)', 'icon': 'hospital', 'color': 'danger', 'is_premium': True, 'order': 7},
    {'name': 'administrativa', 'description': 'Area administrativa (Assistente, Analista)', 'icon': 'briefcase', 'color': 'secondary', 'is_premium': False, 'order': 8},
    {'name': 'ti', 'description': 'Tecnologia da Informacao', 'icon': 'laptop', 'color': 'info', 'is_premium': True, 'order': 9},
    {'name': 'engenharia', 'description': 'Engenharias diversas', 'icon': 'gear-fill', 'color': 'warning', 'is_premium': True, 'order': 10},
    {'name': 'fiscalizacao', 'description': 'Fiscalizacao e regulacao', 'icon': 'clipboard-check', 'color': 'success', 'is_premium': True, 'order': 11},
    {'name': 'logistica', 'description': 'Logistica e transporte', 'icon': 'truck', 'color': 'primary', 'is_premium': True, 'order': 12},
    {'name': 'legislativa', 'description': 'Poder legislativo (Camara, Senado)', 'icon': 'building', 'color': 'secondary', 'is_premium': True, 'order': 13},
    {'name': 'enem_vestibular', 'description': 'ENEM e Vestibulares', 'icon': 'mortarboard-fill', 'color': 'info', 'is_premium': False, 'order': 14},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"  Categoria '{category.get_name_display()}' criada")
    else:
        print(f"  Categoria '{category.get_name_display()}' ja existe")

# Criar modulos
print("\nCriando modulos...")

# Carreiras Policiais
cat_policiais = Category.objects.get(name='policiais')
modulo_pf, _ = Module.objects.get_or_create(
    category=cat_policiais,
    name='Policia Federal - Agente',
    defaults={'description': 'Preparacao para o concurso de Agente da Policia Federal', 'order': 1}
)

disciplinas_pf = [
    {'name': 'Portugues', 'estimated_hours': 80},
    {'name': 'Raciocinio Logico', 'estimated_hours': 60},
    {'name': 'Informatica', 'estimated_hours': 40},
    {'name': 'Direito Constitucional', 'estimated_hours': 70},
    {'name': 'Direito Administrativo', 'estimated_hours': 60},
    {'name': 'Direito Penal', 'estimated_hours': 80},
    {'name': 'Legislacao Especial', 'estimated_hours': 50},
]

for disc_data in disciplinas_pf:
    Subject.objects.get_or_create(
        module=modulo_pf,
        name=disc_data['name'],
        defaults={'estimated_hours': disc_data['estimated_hours'], 'order': disciplinas_pf.index(disc_data) + 1}
    )

print(f"  Modulo '{modulo_pf.name}' com {len(disciplinas_pf)} disciplinas")

# ENEM/Vestibular
cat_enem = Category.objects.get(name='enem_vestibular')
modulo_enem, _ = Module.objects.get_or_create(
    category=cat_enem,
    name='ENEM - Preparacao Completa',
    defaults={'description': 'Todas as areas do conhecimento para o ENEM', 'order': 1}
)

disciplinas_enem = [
    {'name': 'Matematica', 'estimated_hours': 100},
    {'name': 'Portugues', 'estimated_hours': 80},
    {'name': 'Redacao', 'estimated_hours': 60},
    {'name': 'Geografia', 'estimated_hours': 60},
    {'name': 'Historia', 'estimated_hours': 60},
    {'name': 'Fisica', 'estimated_hours': 80},
    {'name': 'Quimica', 'estimated_hours': 80},
    {'name': 'Biologia', 'estimated_hours': 70},
    {'name': 'Literatura', 'estimated_hours': 40},
    {'name': 'Ingles', 'estimated_hours': 40},
]

for disc_data in disciplinas_enem:
    Subject.objects.get_or_create(
        module=modulo_enem,
        name=disc_data['name'],
        defaults={'estimated_hours': disc_data['estimated_hours'], 'order': disciplinas_enem.index(disc_data) + 1}
    )

print(f"  Modulo '{modulo_enem.name}' com {len(disciplinas_enem)} disciplinas")

# Carreiras Bancarias
cat_bancarias = Category.objects.get(name='bancarias')
modulo_bb, _ = Module.objects.get_or_create(
    category=cat_bancarias,
    name='Banco do Brasil - Escriturario',
    defaults={'description': 'Preparacao para concurso do Banco do Brasil', 'order': 1}
)

disciplinas_bb = [
    {'name': 'Portugues', 'estimated_hours': 60},
    {'name': 'Matematica Financeira', 'estimated_hours': 80},
    {'name': 'Raciocinio Logico', 'estimated_hours': 50},
    {'name': 'Informatica', 'estimated_hours': 40},
    {'name': 'Conhecimentos Bancarios', 'estimated_hours': 70},
    {'name': 'Atualidades', 'estimated_hours': 30},
]

for disc_data in disciplinas_bb:
    Subject.objects.get_or_create(
        module=modulo_bb,
        name=disc_data['name'],
        defaults={'estimated_hours': disc_data['estimated_hours'], 'order': disciplinas_bb.index(disc_data) + 1}
    )

print(f"  Modulo '{modulo_bb.name}' com {len(disciplinas_bb)} disciplinas")

print("\nResumo:")
print(f"   - {Category.objects.count()} categorias")
print(f"   - {Module.objects.count()} modulos")
print(f"   - {Subject.objects.count()} disciplinas")
print("\nConcluido!")
