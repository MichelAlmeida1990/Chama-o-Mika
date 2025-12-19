# 🔧 Correção: Bad Request (400) no Backend

## ❌ Problema

Ao tentar acessar o backend no Render, você recebe um erro **Bad Request (400)**.

## 🔍 Causas Comuns

### 1. **ALLOWED_HOSTS não configurado corretamente**

O erro 400 geralmente acontece quando o domínio não está em `ALLOWED_HOSTS`.

**Solução:**

1. No Render Dashboard, vá para **Settings** → **Environment Variables**
2. Verifique se a variável `ALLOWED_HOSTS` está configurada
3. O valor deve ser o domínio do seu backend **SEM** `https://` ou `http://`

**Exemplo correto:**
```
ALLOWED_HOSTS = seu-backend.onrender.com,localhost,127.0.0.1
```

**❌ Errado:**
```
ALLOWED_HOSTS = https://seu-backend.onrender.com  # NÃO inclua https://
ALLOWED_HOSTS = seu-backend.onrender.com, localhost  # NÃO tenha espaços após vírgula
```

### 2. **Espaços em branco nas variáveis**

Se houver espaços após as vírgulas, o Django pode não reconhecer os hosts corretamente.

**Solução:**

O código foi atualizado para remover espaços automaticamente, mas certifique-se de que não há espaços extras ao configurar no Render.

### 3. **CORS não configurado**

Se você está tentando acessar via frontend, o CORS pode estar bloqueando.

**Solução:**

1. Configure `CORS_ALLOWED_ORIGINS` com a URL do seu frontend
2. Use a URL completa com `https://`

**Exemplo:**
```
CORS_ALLOWED_ORIGINS = https://seu-frontend.vercel.app,http://localhost:3000
```

## ✅ Checklist de Verificação

### No Render Dashboard:

- [ ] `ALLOWED_HOSTS` configurado com o domínio do Render (sem https://)
- [ ] `CORS_ALLOWED_ORIGINS` configurado com a URL do frontend (com https://)
- [ ] Sem espaços extras após vírgulas
- [ ] `DEBUG=False` em produção
- [ ] `SECRET_KEY` configurada

### Exemplo Completo de Variáveis:

```
ALLOWED_HOSTS = chama-o-mika-backend.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS = https://chama-o-mika.vercel.app,http://localhost:3000
DEBUG = False
SECRET_KEY = sua-chave-secreta-aqui
SECURE_SSL_REDIRECT = True
```

## 🔍 Como Verificar

1. **Acesse os logs do Render:**
   - Render Dashboard → Seu serviço → **Logs**
   - Procure por erros relacionados a `ALLOWED_HOSTS` ou `DisallowedHost`

2. **Teste a URL diretamente:**
   - Tente acessar: `https://seu-backend.onrender.com/admin/`
   - Se funcionar, o problema pode ser CORS
   - Se não funcionar, verifique `ALLOWED_HOSTS`

## 🚀 Solução Rápida

1. **Render Dashboard** → **Settings** → **Environment Variables**
2. Adicione/Atualize:
   - `ALLOWED_HOSTS` = `seu-backend.onrender.com` (substitua pelo seu domínio)
   - `CORS_ALLOWED_ORIGINS` = `https://seu-frontend.vercel.app` (se tiver frontend)
3. **Salve** e aguarde o restart automático
4. Teste novamente

## 📝 Nota

O código foi atualizado para remover espaços em branco automaticamente de `ALLOWED_HOSTS` e `CORS_ALLOWED_ORIGINS`, mas é importante configurar corretamente no Render.

