# 🔧 Correção: Migrações e ALLOWED_HOSTS

## ❌ Problemas Identificados

Nos logs do Render, aparecem dois erros:

1. **`no such table: auth_user`** - As migrações não foram executadas
2. **`Bad Request (400)`** - ALLOWED_HOSTS não está configurado corretamente

## ✅ Solução

### 1. Verificar Build Command no Render

No Render Dashboard → Settings → Build & Deploy:

**Build Command deve ser:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

⚠️ **IMPORTANTE**: Certifique-se de que o **Root Directory** está configurado como `backend`!

### 2. Configurar ALLOWED_HOSTS

No Render Dashboard → Settings → Environment Variables:

**Adicione/Atualize:**
- **Nome**: `ALLOWED_HOSTS`
- **Valor**: `chama-o-mika-backend.onrender.com,localhost,127.0.0.1`

⚠️ **IMPORTANTE**: 
- NÃO inclua `https://` ou `http://`
- NÃO tenha espaços após as vírgulas
- Use apenas o domínio (ex: `chama-o-mika-backend.onrender.com`)

### 3. Variáveis de Ambiente Completas

Configure todas estas variáveis no Render:

```
SECRET_KEY = sua-chave-secreta-gerada
DEBUG = False
ALLOWED_HOSTS = chama-o-mika-backend.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS = https://seu-frontend.vercel.app,http://localhost:3000
SECURE_SSL_REDIRECT = True
```

### 4. Após Configurar

1. **Salve** todas as variáveis
2. O Render vai **reiniciar automaticamente**
3. Aguarde o deploy completar
4. Teste: `https://chama-o-mika-backend.onrender.com/admin/`

## 🔍 Verificar se Funcionou

Nos logs do Render, você deve ver:
- ✅ `Operations to perform: Apply all migrations`
- ✅ `Running migrations:`
- ✅ `Applying migrations...`
- ✅ Sem erros de `no such table`

E ao acessar a URL, não deve mais aparecer erro 400.

## 📝 Nota

O código já foi atualizado para:
- Remover espaços em branco automaticamente de `ALLOWED_HOSTS`
- Executar migrações no build command
- Tratar erros de banco de dados graciosamente

Mas você ainda precisa configurar as variáveis de ambiente no Render!

