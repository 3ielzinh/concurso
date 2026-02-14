# Configuração do PostgreSQL no Render

## 📋 Passo a Passo

### 1️⃣ Criar Banco de Dados PostgreSQL no Render

1. Acesse [Render Dashboard](https://dashboard.render.com/)
2. Clique em **"New +"** → **"PostgreSQL"**
3. Preencha as informações:
   - **Name**: `concurso-db` (ou o nome que preferir)
   - **Database**: `concurso` (nome do banco)
   - **User**: deixe o padrão ou customize
   - **Region**: escolha a mesma região do seu Web Service (ex: Ohio, Oregon)
   - **PostgreSQL Version**: escolha a versão mais recente (15+)
   - **Plan**: Free (para começar)

4. Clique em **"Create Database"**

### 2️⃣ Obter Credenciais do Banco

Após criar o banco, você verá várias informações na página:

- **Internal Database URL**: use esta se o web service estiver na mesma região
- **External Database URL**: use esta se precisar acessar de fora do Render

A URL tem o formato:
```
postgresql://usuario:senha@host:porta/nome_banco
```

### 3️⃣ Configurar Variáveis de Ambiente no Web Service

No seu **Web Service** do Render:

1. Vá em **"Environment"**
2. Adicione estas variáveis:

```bash
# Database (copie a Internal ou External Database URL)
DATABASE_URL=postgresql://usuario:senha@dpg-xxxx.oregon-postgres.render.com/concurso

# Django Settings
SECRET_KEY=sua-chave-secreta-aqui-gere-uma-nova
DEBUG=False
ALLOWED_HOSTS=concurso-f16y.onrender.com,localhost,127.0.0.1

# Render Hostname (obrigatório para ALLOWED_HOSTS automático)
RENDER_EXTERNAL_HOSTNAME=concurso-f16y.onrender.com
```

### 4️⃣ Variáveis de Ambiente Importantes

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `DATABASE_URL` | URL do PostgreSQL | Copiada do painel do banco PostgreSQL |
| `SECRET_KEY` | String aleatória | Gere com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` | SEMPRE False em produção |
| `ALLOWED_HOSTS` | Domínios permitidos | Lista separada por vírgula |
| `RENDER_EXTERNAL_HOSTNAME` | Seu domínio .onrender.com | Adicionado automaticamente ao ALLOWED_HOSTS |

### 5️⃣ Gerar uma SECRET_KEY Segura

No seu terminal local:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a chave gerada e adicione como variável `SECRET_KEY` no Render.

### 6️⃣ Verificar Conexão do Banco

Após configurar, o Render fará um redeploy automático. Verifique os logs:

1. Vá em **"Logs"** no painel do Web Service
2. Procure por mensagens de sucesso das migrações:
   ```
   Applying contenttypes.0001_initial... OK
   Applying auth.0001_initial... OK
   ...
   ```

### 7️⃣ Criar Superusuário (Opcional)

Para criar um administrador, você pode:

**Opção 1: Via comando no Render**
1. No painel do Web Service, vá em **"Shell"**
2. Execute:
```bash
python manage.py createsuperuser
```

**Opção 2: Criar via código**
Adicione ao seu `populate_data.py` e rode localmente depois faça push:
```python
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin@2026'
    )
```

### ⚠️ Problemas Comuns

#### Erro: "Invalid HTTP_HOST header"
**Solução**: Adicione a variável `RENDER_EXTERNAL_HOSTNAME` com seu domínio

#### Erro: "FATAL: password authentication failed"
**Solução**: Verifique se copiou a `DATABASE_URL` completa e correta

#### Erro: "No such table"
**Solução**: As migrações não rodaram. Verifique o Start Command:
```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi --log-file -
```

#### Banco muito lento
**Solução**: 
- Verifique se o Web Service e o PostgreSQL estão na **mesma região**
- Use a **Internal Database URL** em vez da External

### 📊 Monitoramento

No painel do PostgreSQL, você pode ver:
- **Connections**: quantas conexões ativas
- **Storage Used**: espaço em disco usado
- **Metrics**: gráficos de performance

### 🔄 Backup

O Render faz backups automáticos no plano Free:
- **Daily backups**: mantidos por 7 dias
- Para baixar: vá no painel do PostgreSQL → "Backups"

### 🚀 Próximos Passos

1. ✅ Configure as variáveis de ambiente
2. ✅ Aguarde o redeploy
3. ✅ Teste o login/cadastro
4. ✅ Crie um superusuário
5. ✅ Acesse `/admin` para gerenciar o sistema

### 📝 Checklist Final

- [ ] PostgreSQL criado no Render
- [ ] `DATABASE_URL` configurada no Web Service
- [ ] `SECRET_KEY` forte configurada
- [ ] `DEBUG=False` em produção
- [ ] `RENDER_EXTERNAL_HOSTNAME` configurado
- [ ] Deploy realizado com sucesso
- [ ] Migrações executadas
- [ ] Site acessível e funcionando
- [ ] Superusuário criado

---

## 🎉 Pronto!

Seu sistema agora está rodando com PostgreSQL em produção no Render!

Para qualquer dúvida, consulte a [documentação oficial do Render](https://render.com/docs/databases).
