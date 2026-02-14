"""
Script para criar superusuário para administração
Execute com: python manage.py shell < create_superuser.py
"""

from django.contrib.auth import get_user_model

User = get_user_model()

# Dados do superusuário
username = 'admin'
email = 'admin@concurso.com'
password = 'Admin@2026'

# Verificar se já existe
if User.objects.filter(username=username).exists():
    print(f"⚠️  Usuário '{username}' já existe!")
    user = User.objects.get(username=username)
    print(f"   Email: {user.email}")
    print(f"   É superusuário: {user.is_superuser}")
    print(f"   É staff: {user.is_staff}")
else:
    # Criar superusuário
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='Sistema'
    )
    print("✅ Superusuário criado com sucesso!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\n🔐 Acesse /admin/ com estas credenciais")
