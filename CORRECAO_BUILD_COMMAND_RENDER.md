# 🔧 Correção: Build Command no Render

## ❌ Problema

As migrações não estão sendo executadas porque o **Build Command** no Render está incompleto.

Nos logs, você vê apenas:
```
==> Running build command 'pip install -r requirements.txt'...
```

Mas não vê:
- `python manage.py collectstatic`
- `python manage.py migrate`

## ✅ Solução

### 1. Atualizar Build Command no Render

No **Render Dashboard** → **Settings** → **Build & Deploy**:

**Build Command deve ser:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput --clear && python manage.py migrate --noinput
```

⚠️ **IMPORTANTE**: 
- Certifique-se de que o **Root Directory** está configurado como `backend`
- O comando completo deve estar em uma única linha
- Use `&&` para encadear os comandos

### 2. Passo a Passo

1. Acesse **Render Dashboard**
2. Clique no seu serviço (ex: `chama-o-mika-backend`)
3. Vá em **Settings** (ícone de engrenagem)
4. Role até **Build & Deploy**
5. Encontre o campo **Build Command**
6. **Substitua** o comando atual por:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput --clear && python manage.py migrate --noinput
   ```
7. Clique em **Save Changes**
8. O Render vai fazer um novo deploy automaticamente

### 3. Verificar se Funcionou

Após o deploy, nos logs você deve ver:

```
==> Running build command 'pip install -r requirements.txt && python manage.py collectstatic --noinput --clear && python manage.py migrate --noinput'...
...
Successfully installed ...
...
Copying '/opt/render/project/src/backend/...'
...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, estoque, financeiro
Running migrations:
  Applying migrations...
  [OK] ...
```

E **NÃO** deve mais aparecer:
- ❌ `no such table: auth_user`
- ❌ `⚠️ Erro ao criar superusuário`

### 4. Após as Migrações

Depois que as migrações rodarem com sucesso:

1. Configure `ALLOWED_HOSTS` (se ainda não configurou):
   - `ALLOWED_HOSTS = chama-o-mika-backend.onrender.com,localhost,127.0.0.1`

2. Configure `MAKE_SUPERUSER` (se quiser tornar o usuário superusuário):
   - `MAKE_SUPERUSER = rafael@chamaomika.com`

3. Teste o admin:
   - `https://chama-o-mika-backend.onrender.com/admin/`

## 📝 Nota

O Build Command correto executa 3 etapas:
1. **Instala dependências**: `pip install -r requirements.txt`
2. **Coleta arquivos estáticos**: `python manage.py collectstatic --noinput --clear`
3. **Executa migrações**: `python manage.py migrate --noinput`

Todas as 3 etapas são necessárias para o deploy funcionar corretamente!

