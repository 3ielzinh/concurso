# Criar Superusuário no Render

## 🔐 Método Recomendado: Via Shell do Render

### Passo 1: Acessar Shell
1. Acesse o [Dashboard do Render](https://dashboard.render.com/)
2. Clique no seu **Web Service** (concurso-f16y)
3. No menu lateral, clique em **"Shell"**

### Passo 2: Executar Comando
No shell que abrir, execute:

```bash
python manage.py createsuperuser
```

### Passo 3: Preencher Dados
Será solicitado:
- **Username**: `admin` (ou o que preferir)
- **Email**: `admin@concurso.com`
- **Password**: Crie uma senha forte
- **Password (again)**: Repita a senha

### Passo 4: Acessar Admin
Acesse: https://concurso-f16y.onrender.com/admin/

Use as credenciais que você criou.

---

## 📝 Alternativa: Via Script Python no Shell

Cole este código no Shell do Render:

```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Verificar se já existe
if User.objects.filter(username='admin').exists():
    print('Usuario admin ja existe!')
else:
    user = User.objects.create_superuser(
        username='admin',
        email='admin@concurso.com',
        password='SuaSenhaForte123!',
        first_name='Admin',
        last_name='Sistema'
    )
    print('Superusuario criado com sucesso!')
```

---

## 🎯 Superusuário Local

Para desenvolvimento local, já existe um superusuário:
- **Username**: `admin`
- **Password**: `Admin@2026`
- **URL**: http://localhost:8000/admin/

---

## ⚙️ Opção: Adicionar ao populate_data.py

Se quiser que o superusuário seja criado automaticamente no deploy, adicione ao final do arquivo `populate_data.py`:

```python
# Criar superusuário padrão
print("\n👤 Criando superusuário...")
admin_username = 'admin'
admin_email = 'admin@concurso.com'
admin_password = 'Admin@2026!'

if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        first_name='Admin',
        last_name='Sistema'
    )
    print(f"  ✅ Superusuário '{admin_username}' criado")
else:
    print(f"  ℹ️  Superusuário '{admin_username}' já existe")
```

⚠️ **Importante**: Troque a senha padrão após o primeiro acesso!
