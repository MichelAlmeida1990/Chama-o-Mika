# 🔧 Solução: Erros 401 e 403 - Problemas de Autenticação

## ❌ Problemas Identificados

- **401 Unauthorized** em `/api/auth/user/` - Usuário não autenticado
- **403 Forbidden** em `/api/produtos/`, `/api/categorias/` - Sem permissão (não autenticado)

## 🔍 Causa

A sessão não está sendo mantida entre o frontend (Vercel) e o backend (Render) devido a configurações de cookies cross-domain.

## ✅ Soluções

### 1. Verificar CORS_ALLOWED_ORIGINS no Render

**No Render Dashboard** → **Settings** → **Environment Variables**:

Verifique se `CORS_ALLOWED_ORIGINS` está configurado com a URL do seu frontend:

```
CORS_ALLOWED_ORIGINS = https://chama-o-mika.vercel.app,http://localhost:3000
```

⚠️ **IMPORTANTE**:
- Use a URL completa com `https://`
- Separe múltiplas URLs por vírgula
- Não tenha espaços após vírgulas

### 2. Verificar CSRF_TRUSTED_ORIGINS

O código já configura automaticamente, mas certifique-se de que `CORS_ALLOWED_ORIGINS` está correto.

### 3. Fazer Login Novamente

Após configurar o CORS:

1. **Limpe os cookies do navegador**:
   - Chrome: F12 → Application → Cookies → Delete All
   - Ou use modo anônimo

2. **Acesse o frontend**: `https://chama-o-mika.vercel.app`

3. **Faça login**:
   - Username: `admin`
   - Password: `admin123`

4. **Verifique se funcionou**:
   - O dashboard deve carregar
   - Não deve mais aparecer erros 401/403

### 4. Verificar Configurações de Sessão

As configurações já foram atualizadas no código:
- `SESSION_COOKIE_SAMESITE = 'None'` (permite cross-domain)
- `SESSION_COOKIE_SECURE = True` (apenas HTTPS)
- `CSRF_COOKIE_SAMESITE = 'None'`

### 5. Se Ainda Não Funcionar

**Opção A - Verificar se o frontend está enviando cookies:**

No console do navegador (F12), verifique:
- Network → Headers → Request Headers
- Deve ter `Cookie: sessionid=...`

**Opção B - Verificar CORS no backend:**

Nos logs do Render, verifique se há erros de CORS.

**Opção C - Testar login diretamente:**

```bash
curl -X POST https://chama-o-mika-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  -c cookies.txt -v
```

Se retornar `"success": true`, o login está funcionando.

## 📝 Checklist

- [ ] `CORS_ALLOWED_ORIGINS` configurado com URL do Vercel
- [ ] `ALLOWED_HOSTS` configurado com domínio do Render
- [ ] Cookies limpos no navegador
- [ ] Login feito novamente após limpar cookies
- [ ] Frontend acessando a URL correta do backend

## 🔍 Como Verificar se Está Funcionando

1. **Acesse o frontend**: `https://chama-o-mika.vercel.app`
2. **Abra o DevTools** (F12)
3. **Vá em Network**
4. **Faça login**
5. **Verifique a requisição `/api/auth/login/`**:
   - Status deve ser `200`
   - Response deve ter `"success": true`
6. **Verifique requisições subsequentes**:
   - `/api/auth/user/` deve retornar `200`
   - `/api/produtos/` deve retornar `200` (não 403)

## ⚠️ Importante

Se você mudou `CORS_ALLOWED_ORIGINS` no Render:
1. **Salve** as alterações
2. **Aguarde o restart** automático
3. **Limpe os cookies** do navegador
4. **Faça login novamente**

